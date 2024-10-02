from enum import Enum


class OwnerTypes(str, Enum):
    User = "user"
    Tenant = "tenant"

    def __str__(self):
        return self.value
