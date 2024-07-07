from enum import Enum


class MachinesWaitState(str, Enum):
    DESTROYED = "destroyed"
    STARTED = "started"
    STOPPED = "stopped"

    def __str__(self) -> str:
        return str(self.value)
