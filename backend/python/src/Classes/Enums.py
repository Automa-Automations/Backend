from enum import Enum


class BotType(Enum):
    AiImageGeneration = "AiImageGeneration"


class Platform(Enum):
    Instagram = "Instagram"


class PostPublicity(Enum):
    PUBLIC = "Public"
    PRIVATE = "Private"
    UNLISTED = "Unlisted"
