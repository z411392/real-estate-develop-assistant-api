from enum import Enum


class RegistryStatuses(str, Enum):
    Pending = "pending"
    Doing = "doing"
    Done = "done"
    Failed = "failed"

    def __str__(self):
        return self.value
