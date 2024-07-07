from enum import Enum


class FlyMachineRestartPolicy(str, Enum):
    ALWAYS = "always"
    NO = "no"
    ON_FAILURE = "on-failure"

    def __str__(self) -> str:
        return str(self.value)
