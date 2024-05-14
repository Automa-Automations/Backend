from comfy_script.runtime import Checkpoints, Workflow, CheckpointLoaderSimple, CLIPTextEncode, EmptyLatentImage, KSampler, VAEDecode, SaveImage
import dataclasses
from typing import Tuple

@dataclasses.dataclass
class GenerateRequest:
    id: str
    model: str
    prompt: str
    negative_prompt: str
    size: Tuple[int, int]
    batch_size: int
    seed: int
    steps: int
    guide: float
    parser: str = "euler"
    scheduler: str = "normal"
    denoise: bool = False

def list_models() -> list[str]:
    return [m.value for m in Checkpoints]

def generate(input: GenerateRequest) -> list[str]:
    with Workflow():
        model, clip, vae = CheckpointLoaderSimple(input.model)
        conditioning = CLIPTextEncode(input.prompt, clip)
        conditioning2 = CLIPTextEncode(input.negative_prompt, clip)
        latent = EmptyLatentImage(input.size[0], input.size[1], input.batch_size)
        latent = KSampler(model, input.seed, input.steps, input.guide, input.parser, input.scheduler, conditioning, conditioning2, latent, input.denoise)
        image = VAEDecode(latent, vae)
        SaveImage(image, input.id)
        return [input.id]
