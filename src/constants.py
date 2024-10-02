from enum import Enum
from os import getenv


Version = "0.0.1.20241003"


class DatetimeFormats(str, Enum):
    ISO8601DATE = r"%Y-%m-%d"
    ISO8601TIME = r"%H:%M:%S"
    ISO8601 = r"%Y-%m-%d %H:%M:%S"

    def __str__(self):
        return self.value


class PageSizes(int, Enum):
    Tenants = 20
    Snapshots = 20


class Collections(str, Enum):
    Tenants = "tenants"
    Permissions = "permissions"
    Ownerships = "ownerships"
    Snapshots = "snapshots"
    Registries = "registries"

    def __str__(self):
        prefix = getenv("ENV")
        return f"{prefix}_{self.value}" if prefix else self.value


Root = "TWnYURxLxWSNtBOI3Y2936kPyrg1"
