from enum import Enum


class SnapshotTypes(str, Enum):
    Building = "building"
    Land = "land"

    def __str__(self):
        return self.value
