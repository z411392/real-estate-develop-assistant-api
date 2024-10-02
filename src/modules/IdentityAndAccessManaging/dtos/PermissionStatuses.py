from enum import Enum


class PermissionStatuses(str, Enum):
    Pending = "pending"
    Approved = "approved"
    Rejected = "rejected"

    def __str__(self):
        return self.value
