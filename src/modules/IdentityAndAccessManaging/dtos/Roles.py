from enum import Enum


class Roles(str, Enum):
    Owner = "owner"
    Member = "member"

    def __str__(self):
        return self.value
