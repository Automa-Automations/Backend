from enum import Enum


class FlyEnvFromFieldRef(str, Enum):
    APP_NAME = "app_name"
    ID = "id"
    IMAGE = "image"
    PRIVATE_IP = "private_ip"
    REGION = "region"
    VERSION = "version"

    def __str__(self) -> str:
        return str(self.value)
