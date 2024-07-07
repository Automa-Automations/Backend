from enum import Enum


class MachineHostStatus(str, Enum):
    OK = "ok"
    UNKNOWN = "unknown"
    UNREACHABLE = "unreachable"

    def __str__(self) -> str:
        return str(self.value)
