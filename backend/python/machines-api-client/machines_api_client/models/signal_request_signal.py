from enum import Enum


class SignalRequestSignal(str, Enum):
    SIGABRT = "SIGABRT"
    SIGALRM = "SIGALRM"
    SIGFPE = "SIGFPE"
    SIGHUP = "SIGHUP"
    SIGILL = "SIGILL"
    SIGINT = "SIGINT"
    SIGKILL = "SIGKILL"
    SIGPIPE = "SIGPIPE"
    SIGQUIT = "SIGQUIT"
    SIGSEGV = "SIGSEGV"
    SIGTERM = "SIGTERM"
    SIGTRAP = "SIGTRAP"
    SIGUSR1 = "SIGUSR1"

    def __str__(self) -> str:
        return str(self.value)
