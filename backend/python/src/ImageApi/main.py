# This will be the main entrypoint for the image generator api.
# This will run through the entire startup script, ensuring everything is installed.
# And then leverage functionality via a "get_client()" property!
import base64
from enum import Enum
from io import BytesIO

from craiyon import Craiyon, craiyon_utils
from PIL import Image
from pydantic import BaseModel, HttpUrl


class ImageAIModelTypes(Enum):
    AUTO = "auto"
    COMFYUI = "comfyui"
    DALLE_MINI = "dalle_mini"
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


class ImageGenerationResponse(BaseModel):
    final_prompt: ImageGenerationPrompt
    output_images: list[bytes]
    steps: list[str] = []


class ImageAPI:
    @classmethod
    def generate(cls, input: ImageGenerationInput) -> ImageGenerationResponse | None:
        match input.gen_model_type:
            case ImageAIModelTypes.AUTO:
                print("Use Other Parameters to do Generations...")
            case ImageAIModelTypes.COMFYUI:
                print(
                    "Use ComfyUI based workflow Generation to Generate Image (Move over to AUTO if no comfy baseline)"
                )
            case ImageAIModelTypes.DALLE_MINI:
                print("Generate Image using DALLE-MINI")
                return cls._dalle_mini_generator(input.prompt)
            case ImageAIModelTypes.CLAID:
                print("Generating Images using Claid (product based api)")
            case _:
                raise Exception("Invalid Option")

        return None

    @classmethod
    def _dalle_mini_generator(
        cls, prompt: ImageGenerationPrompt | str
    ) -> ImageGenerationResponse:
        generator = Craiyon()
        enhanced_prompt = ImageGenerationPrompt(positive_prompt="", negative_prompt="")
        if isinstance(prompt, str):
            enhanced_prompt = cls._enhance_prompt(prompt)
        elif prompt.enhance:
            enhanced_prompt = cls._enhance_prompt(prompt)
        else:
            enhanced_prompt = prompt

        result = generator.generate(
            prompt=enhanced_prompt.positive_prompt,
            negative_prompt=enhanced_prompt.negative_prompt,
            model_type=(
                (enhanced_prompt.style).value
                if enhanced_prompt.style != ImageAIStyleTypes.AUTO
                else "none"
            ),
        )
        images = craiyon_utils.encode_base64(result.images)

        return ImageGenerationResponse(
            final_prompt=enhanced_prompt,
            output_images=images,
        )

    @classmethod
    def _enhance_prompt(
        cls, prompt: ImageGenerationPrompt | str
    ) -> ImageGenerationPrompt:
        if isinstance(prompt, str):
            return ImageGenerationPrompt(
                positive_prompt=prompt,
                negative_prompt="ugly, misfigured, bad artist, words",
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
        gen_model_type=ImageAIModelTypes.DALLE_MINI,
    )
    images = ImageAPI.generate(input)

    if not images:
        raise Exception("Invalid Model")

    for index, i in enumerate(images.output_images):
        image = Image.open(BytesIO(base64.decodebytes(i)))
        image.convert("RGBA").save(f"/tmp/{index}-generation.png", "PNG")
