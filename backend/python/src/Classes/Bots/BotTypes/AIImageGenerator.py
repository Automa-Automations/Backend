import uuid
from dataclasses import dataclass
from typing import Tuple, List

from src.Classes.Bot import client
from src.Classes.ContentGenerationBotHandler import ContentGenerationBotHandler
from src.Classes.Enums import PostPublicity
from src.Classes.User import DatabaseSyncedProfile
from src.ai.ImageApi import ImageApi


@dataclass
class AiImageGenerationBotMetadata():
    """AiImageGenerationBotMetadata: The metadata for the AiImageGeneration bot."""
    model: str
    """str: The model to use for generating the image."""

    style: str
    """str: The style to use for generating the image."""

    size: Tuple[int, int]
    """str: The size of the image to generate."""

    negative_prompt: str
    """str: The negative prompt to use for generating the image."""

    positive_prompt: str
    """str: The positive prompt to use for generating the image."""

    title_prompt: str
    """str: The title prompt to use for generating the image."""

    description_prompt: str
    """str: The description prompt to use for generating the image."""

    total_images: int
    """int: The total number of images to generate."""

    base_topic: str
    """str: The base topic of the images. This is like the main driver of what should be generated!"""


class AIImageGenerationBotHandler(ContentGenerationBotHandler):
    """AIImageGenerationBot: The AI Image Generation bot class. This class will provide all of the methods to interact with the AI Image Generation bot."""

    metadata: AiImageGenerationBotMetadata
    """AiImageGenerationBotMetadata: The metadata of the bot."""

    def _generate_topic_item(self, base_topic: str):
        return client.generate(
            model="phi3:3.8b",
            prompt=f"Please generate a 1-3 word topic based on the base_topic provided: {base_topic}. You should only respond with the response, no extra fluff attached to the message, for example <BASE_TOPIC>, your response: Cute ginger cat. Only respond with the answer in the format  have given you!",
            keep_alive="1m"
        )["response"]

    def _generate_image_prompt(self, base_prompt: str, topic: str, style: str):
        return client.generate(
            model="phi3:3.8b",
            prompt=f'{base_prompt} The topic for the image should be: {topic}. And the stile reference should be {style}. Give us a descriptive image prompt that will allow the AI image generator to generate a high quality image! Limit your propmpt to 2 sentences, and only respond with the image prompt, No extra context before or after, for example: MY INPUT, your output: "very cute tiny, A cute orange cat smile wearing sweater avatar, rim lighting, adorable big eyes, small, By greg rutkowski, chibi, Perfect lighting, Sharp focus"',
            keep_alive="1m"
        )["response"]

    def _generate_image_title(self, base_title: str, topic: str, style: str):
        return client.generate(
            model="phi3:3.8b",
            prompt=f'{base_title} The topic for the image should be: {topic}. And the stile reference should be {style}. Give us a descriptive image title that will allow the AI image generator to generate a high quality image! Limit your title to 2 sentences, and only respond with the image title, No extra context before or after, for example: MY INPUT, your output: "Cute orange cat smile wearing sweater avatar, rim lighting, adorable big eyes, small, By greg rutkowski, chibi, Perfect lighting, Sharp focus. Ensure you are fully exclaiming the main topic of the image, as we dont want the AI to generate an image that is invalid."',
            keep_alive='1m'
        )["response"]

    def _generate_image_description(
        self, base_title: str, topic: str, style: str
    ):
        return client.generate(
            model="phi3:3.8b",
            prompt=f'{base_title} The topic for the image should be: {topic}. And the stile reference should be {style}. Give us a descriptive image description that will allow the AI image generator to generate a high quality image! Limit your description to 10 sentences, max, and 1 sentence min, only respond with the image description, No extra context before or after, for example: MY INPUT, your output: "Cute orange cat smile wearing sweater avatar, rim lighting, adorable big eyes, small, By greg rutkowski, chibi, Perfect lighting, Sharp focus... REST OF RESPONSE ... Check out my socials ... #something, something something! . Ensure you are fully exclaiming the main topic of the image, as we dont want the AI to generate an image that is invalid."',
            keep_alive='1m'
        )["response"]

    def _generate_image(
        self, prompt: str, negative_prompt: str, model: str, size: tuple
    ):
        api = ImageApi()
        return api.generate_image(
            prompt, negative_prompt, model, size[0], size[1]
        )

    def generate(self, owner: DatabaseSyncedProfile) -> List['Post']:
        posts = []
        for i in range(self.metadata.total_images):
            # It costs 1 credit per image
            if  owner.credits < 1:
                raise Exception("Not enough credits to generate images!")

            owner.credits -= 1

            print("Generating topic...")
            topic = self._generate_topic_item(self.metadata.base_topic).split('\n')[0].strip()
            print("Generated topic: ", topic)

            print("Generating prompt...")
            prompt = self._generate_image_prompt(
                self.metadata.positive_prompt, topic, self.metadata.style
            ).strip()
            print("Generated prompt: ", prompt)

            print("Generating title...")
            title = self._generate_image_title(
                self.metadata.title_prompt
                + f"Here is the prompt for the generated image, you can also use this as reference! {prompt}".format(
                    prompt=prompt
                ),
                topic,
                self.metadata.style,
            ).strip()
            print("Generated title: ", title)

            print("Generating description...")
            description = self._generate_image_description(
                title,
                topic + "\nImage Prompt: {prompt}".format(prompt=prompt),
                self.metadata.style,
            ).strip()
            print("Generated description: ", description)

            print("Generating image...")
            images = self._generate_image(
                prompt,
                self.metadata.negative_prompt,
                self.metadata.model,
                self.metadata.size,
            )
            print("Generated image: ", len(images))
            image_filepath = f"/tmp/{i}_{uuid.uuid4().hex}.png"
            with open(image_filepath, "wb") as f:
                f.write(images[0])

            posts.append(Post(title=title, description=description, tags=[], publicity=PostPublicity.PUBLIC, content=image_filepath))

        return posts
