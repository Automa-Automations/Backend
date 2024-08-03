# This will be the main entrypoint for the image generator api.
# This will run through the entire startup script, ensuring everything is installed.
# And then leverage functionality via a "get_client()" property!
import base64
import os
from enum import Enum
from io import BytesIO

import requests
from PIL import Image
from pydantic import BaseModel, HttpUrl


class ImageAIModelTypes(Enum):
    AUTO = "auto"
    COMFYUI = "comfyui"
    MINI = "mini"
    CLAID = "product"


class ImageAIStyleTypes(Enum):
    AUTO = "auto"
    ART = "art"
    DRAWING = "drawing"
    PHOTO = "photo"
    NONE = "none"


class ImageGenerationComfyUIInput(BaseModel):
    comfyui_workflow_id: str
    comfyui_workflow_json: str | None
    comfyui_workflow_url: HttpUrl | None


class ImageGenerationPrompt(BaseModel):
    positive_prompt: str
    negative_prompt: str
    enhance: bool = False
    style: ImageAIStyleTypes = ImageAIStyleTypes.AUTO


class ImageGenerationInput(BaseModel):
    prompt: ImageGenerationPrompt | str
    comfyui: ImageGenerationComfyUIInput | None = None
    gen_model_type: ImageAIModelTypes = ImageAIModelTypes.AUTO
    debug: bool = False


class ImageGenerationResponse(BaseModel):
    final_prompt: ImageGenerationPrompt
    output_images: list[str]
    steps: list[str] = []


class ImageAPI:
    @classmethod
    def generate(cls, input: ImageGenerationInput) -> ImageGenerationResponse | None:
        match input.gen_model_type:
            case ImageAIModelTypes.AUTO:
                print("Use Other Parameters to do Generations...")
                return cls._mini_generator(input.prompt)
            case ImageAIModelTypes.COMFYUI:
                print(
                    "Use ComfyUI based workflow Generation to Generate Image (Move over to AUTO if no comfy baseline)"
                )
            case ImageAIModelTypes.MINI:
                print("Generate Image using SD1 from HuggingFace")
                return cls._mini_generator(input.prompt)
            case ImageAIModelTypes.CLAID:
                print("Generating Images using Claid (product based api)")
            case _:
                raise Exception("Invalid Option")

        return None

    @classmethod
    def _mini_generator(
        cls, prompt: ImageGenerationPrompt | str
    ) -> ImageGenerationResponse:
        enhanced_prompt = ImageGenerationPrompt(positive_prompt="", negative_prompt="")
        if isinstance(prompt, str):
            enhanced_prompt = cls._enhance_prompt(prompt)
        elif prompt.enhance:
            enhanced_prompt = cls._enhance_prompt(prompt)
        else:
            enhanced_prompt = prompt

        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        headers = {"Authorization": f"Bearer {os.environ['HUGGING_FACE_API_TOKEN']}"}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.content

        image_bytes = query(
            {
                "inputs": f"POSITIVE: {enhanced_prompt.positive_prompt} || NEGATIVE {enhanced_prompt.negative_prompt}",
            }
        )

        return ImageGenerationResponse(
            final_prompt=enhanced_prompt,
            output_images=[base64.b64encode(image_bytes).decode("utf-8")],
        )

    @classmethod
    def _enhance_prompt(
        cls, prompt: ImageGenerationPrompt | str
    ) -> ImageGenerationPrompt:
        if isinstance(prompt, str):
            return ImageGenerationPrompt(
                positive_prompt=prompt,
                negative_prompt="ugly, misfigured, bad artist, words",
                enhance=True,
            )
        else:
            return prompt


if __name__ == "__main__":
    input = ImageGenerationInput(
        prompt=ImageGenerationPrompt(
            positive_prompt="furball",
            negative_prompt="ugly, misfigured, bad artist, words",
            style=ImageAIStyleTypes.ART,
        ),
        gen_model_type=ImageAIModelTypes.MINI,
    )
    images = ImageAPI.generate(input)

    if not images:
        raise Exception("Invalid Model")

    for index, i in enumerate(images.output_images):
        image = Image.open(BytesIO(base64.decodebytes(i)))
        image.convert("RGBA").save(f"/tmp/{index}-generation.png", "PNG")
