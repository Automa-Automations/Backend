from ollama import Client
from src.ai.ImageApi import ImageApi
client = Client(host='http://localhost:11434')

def generate_topic_item(base_topic: str):
    return client.generate(model='llama3', prompt=f'Please generate a 1-3 word topic based on the base_topic provided: {base_topic}. You should only respond with the response, no extra fluff attached to the message, for example <BASE_TOPIC>, your response: Cute ginger cat')['response']


def generate_image_prompt(base_prompt: str, topic: str, style: str):
    return client.generate(model='llama3', prompt=f'{base_prompt} The topic for the image should be: {topic}. And the stile reference should be {style}. Give us a descriptive image prompt that will allow the AI image generator to generate a high quality image! Limit your propmpt to 2 sentences, and only respond with the image prompt, No extra context before or after, for example: MY INPUT, your output: "very cute tiny, A cute orange cat smile wearing sweater avatar, rim lighting, adorable big eyes, small, By greg rutkowski, chibi, Perfect lighting, Sharp focus"')['response']

def generate_image_title(base_title: str, topic: str, style: str):
    return client.generate(model='llama3', prompt=f'{base_title} The topic for the image should be: {topic}. And the stile reference should be {style}. Give us a descriptive image title that will allow the AI image generator to generate a high quality image! Limit your title to 2 sentences, and only respond with the image title, No extra context before or after, for example: MY INPUT, your output: "Cute orange cat smile wearing sweater avatar, rim lighting, adorable big eyes, small, By greg rutkowski, chibi, Perfect lighting, Sharp focus"')['response']

def generate_image(prompt: str, negative_prompt: str, model: str, size: tuple):
    api = ImageApi()
    return api.generate_image(prompt, negative_prompt, model, size[0], size[1])
    
def upload_image(botId: str, images: list[bytes], title: str) -> None:
    from instagrapi import Client
    cl = Client()
    cl.login("adoniscodes_", "Simon...!23")

    for image in images:
        # Save image to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
            temp.write(image)
            temp.flush()
            temp.seek(0)

            media = cl.photo_upload(
                temp.name,
                "Test caption for photo with #hashtags and mention users such @example",
                extra_data={
                    "custom_accessibility_caption": "alt text example",
                    "like_and_view_counts_disabled": 1,
                    "disable_comments": 1,
                }
            )
            print(media.model_dump()['code'])
