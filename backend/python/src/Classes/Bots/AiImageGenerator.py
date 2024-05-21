import dataclasses
import datetime
import json
import instagrapi
from ollama import Client
from src.ai.ImageApi import ImageApi
from typing import Optional, Tuple
import os

from src.utils import get_value

client = Client(host="http://localhost:11434")

@dataclasses.dataclass
class Proxy:
    id: int
    created_at: datetime.datetime
    host: str
    port: int
    type_: str
    security: str
    username: str
    password: str
    country: str

    @classmethod
    def from_dict(cls, dict_: dict):
        return Proxy(**dict_)

    @classmethod
    def from_id(cls, id: int):
        table = "proxies"
        value = get_value(table=table, line=id)
        cls.from_dict(value)





@dataclasses.dataclass
class AiImageGenerator:
    id: int
    created_at: datetime.datetime
    owner_id: str
    username: str
    password: str
    session: dict
    proxy_id: int
    metadata: dict
    configuration: dict
    type_: str
    platform: str

    def _generate_topic_item(self, base_topic: str):
        return client.generate(
            model="llama3",
            prompt=f"Please generate a 1-3 word topic based on the base_topic provided: {base_topic}. You should only respond with the response, no extra fluff attached to the message, for example <BASE_TOPIC>, your response: Cute ginger cat",
        )["response"]

    def _generate_image_prompt(self, base_prompt: str, topic: str, style: str):
        return client.generate(
            model="llama3",
            prompt=f'{base_prompt} The topic for the image should be: {topic}. And the stile reference should be {style}. Give us a descriptive image prompt that will allow the AI image generator to generate a high quality image! Limit your propmpt to 2 sentences, and only respond with the image prompt, No extra context before or after, for example: MY INPUT, your output: "very cute tiny, A cute orange cat smile wearing sweater avatar, rim lighting, adorable big eyes, small, By greg rutkowski, chibi, Perfect lighting, Sharp focus"',
        )["response"]

    def _generate_image_title(self, base_title: str, topic: str, style: str):
        return client.generate(
            model="llama3",
            prompt=f'{base_title} The topic for the image should be: {topic}. And the stile reference should be {style}. Give us a descriptive image title that will allow the AI image generator to generate a high quality image! Limit your title to 2 sentences, and only respond with the image title, No extra context before or after, for example: MY INPUT, your output: "Cute orange cat smile wearing sweater avatar, rim lighting, adorable big eyes, small, By greg rutkowski, chibi, Perfect lighting, Sharp focus"',
        )["response"]

    def _generate_image_description(
        self, base_title: str, topic: str, style: str
    ):
        return client.generate(
            model="llama3",
            prompt=f'{base_title} The topic for the image should be: {topic}. And the stile reference should be {style}. Give us a descriptive image description that will allow the AI image generator to generate a high quality image! Limit your description to 10 sentences, max, and 1 sentence min, only respond with the image description, No extra context before or after, for example: MY INPUT, your output: "Cute orange cat smile wearing sweater avatar, rim lighting, adorable big eyes, small, By greg rutkowski, chibi, Perfect lighting, Sharp focus... REST OF RESPONSE ... Check out my socials ... #something, something something!"',
        )["response"]

    def _generate_image(
        self, prompt: str, negative_prompt: str, model: str, size: tuple
    ):
        api = ImageApi()
        return api.generate_image(
            prompt, negative_prompt, model, size[0], size[1]
        )

    def generate(self):
        print("Generating topic...")
        topic = self._generate_topic_item(self.metadata["base_topic"])
        print("Generated topic: ", topic)

        print("Generating prompt...")
        prompt = self._generate_image_prompt(
            self.metadata["base_prompt"], topic, self.metadata["style"]
        )
        print("Generated prompt: ", prompt)
    
        print("Generating title...")
        title = self._generate_image_title(
            self.metadata["base_title"]
            + f"Here is the prompt for the generated image, you can also use this as reference! {prompt}".format(
                prompt=prompt
            ),
            topic,
            self.metadata["style"],
        )
        print("Generated title: ", title)
    
        print("Generating description...")
        description = self._generate_image_description(
            title,
            topic + "\nImage Prompt: {prompt}".format(prompt=prompt),
            self.metadata["style"],
        )
        print("Generated description: ", description)

        print("Generating image...")
        images = self._generate_image(
            prompt,
            self.metadata["negative_prompt"],
            self.metadata["model"],
            self.metadata["size"],
        )
        print("Generated image: ", len(images))
        return title, topic, prompt, description, images

    def upload(self, title, topic, prompt, description, images) -> str:
        pass

    @property
    def proxy(self):
        return Proxy.from_id(id=self.proxy_id)

    @property
    def session_file_path(self) -> Tuple[str, bool]:
        filename = f"/tmp/{self.id}.json"
        if os.path.exists(filename):
            return filename, True
        else:
            return filename, False

    @classmethod
    def from_dict(cls, dict_: dict, type_):
        return type_(**dict_)

    @classmethod
    def from_id(cls, id: int, type_):
        table = "bots"
        value = get_value(table=table, line=id)
        return cls.from_dict(value, type_)

        


class Instagram(AiImageGenerator):
    _client: Optional[instagrapi.Client]

    @property
    def client(self) -> instagrapi.Client:
        if getattr(self, "_client", None):
            return self._client
        else:
            self._client = instagrapi.Client()
            return self._client

    def upload(self, title, topic, prompt, description, images) -> str:
        cl = self.client
        cl.set_proxy(self.proxy)
        session_filepath, exists = self.session_file_path
        if exists:
            cl.load_settings(session_filepath)
        else:
            cl.login(self.username, self.password)
            cl.dump_settings(session_filepath)
            with open(session_filepath, "r") as f:
                content = json.load(f)
                self.session = content

        for image in images:
            import tempfile

            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".jpg"
            ) as temp:
                temp.write(image)
                temp.flush()
                temp.seek(0)

                media = cl.photo_upload(
                    temp.name,
                    title
                    + "\n\n{description}".format(description=description),
                )
                print(media)
            

