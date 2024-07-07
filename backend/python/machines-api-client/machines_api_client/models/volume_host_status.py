from enum import Enum


class VolumeHostStatus(str, Enum):
    OK = "ok"
    UNKNOWN = "unknown"
    UNREACHABLE = "unreachable"

    def __str__(self) -> str:
        return str(self.value)
