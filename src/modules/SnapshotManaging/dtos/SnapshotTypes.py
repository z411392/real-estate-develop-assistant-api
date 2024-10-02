from enum import Enum


class SnapshotTypes(str, Enum):
    Buildings = "building"
    Lands = "lands"

    def __str__(self):
        return self.value
