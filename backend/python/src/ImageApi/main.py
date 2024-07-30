# This will be the main entrypoint for the image generator api.
# This will run through the entire startup script, ensuring everything is installed.
# And then leverage functionality via a "get_client()" property!
from enum import Enum

from pydantic import BaseModel, HttpUrl, StringConstraints


class ImageAIModelTypes(Enum):
    COMFYUI = "comfyui"
    DALLE_MINI = "dalle_mini"
    CLAID = "product"
    AUTO = "auto"


class ImageGenerationComfyUIInput(BaseModel):
    comfyui_workflow_id: str
    comfyui_workflow_json: str | None
    comfyui_workflow_url: HttpUrl | None


class ImageGenerationPrompt(BaseModel):
    positive_prompt: str
    negative_prompt: str
    enhance: bool = False


class ImageGenerationInput(BaseModel):
    prompt: ImageGenerationPrompt | str
    comfyui: ImageGenerationComfyUIInput | None
    model_type: ImageAIModelTypes = ImageAIModelTypes.AUTO


class ImageAPI:
    @staticmethod
    def generate(input: ImageGenerationInput):
        match input.model_type:
            case ImageAIModelTypes.AUTO:
                print("Use Other Parameters to do Generations...")
            case ImageAIModelTypes.COMFYUI:
                print(
                    "Use ComfyUI based workflow Generation to Generate Image (Move over to AUTO if no comfy baseline)"
                )
            case ImageAIModelTypes.DALLE_MINI:
                print("Generate Image using DALLE-MINI")
            case ImageAIModelTypes.CLAID:
                print("Generating Images using Claid (product based api)")
            case _:
                raise Exception("Invalid Option")

    @classmethod
    def _dalle_mini_generator(cls, prompt: ImageGenerationPrompt | str):
        enhanced_prompt = ""
        if isinstance(prompt, str):
            # Do Prompt Enhancement
            ...

    @classmethod
    def _enhance_prompt(
        cls, prompt: ImageGenerationPrompt | str
    ) -> ImageGenerationPrompt:
        if isinstance(prompt, str):
            ...
