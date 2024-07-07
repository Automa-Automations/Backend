from enum import Enum


class MainStatusCode(str, Enum):
    INSUFFICIENT_CAPACITY = "insufficient_capacity"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
