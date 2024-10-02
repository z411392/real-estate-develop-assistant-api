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
    Users = 20


class Collections(str, Enum):
    Tenants = "tenants"
    Permissions = "permissions"
    Ownerships = "ownerships"
    Snapshots = "snapshots"
    SnapshotEvents = "snapshots/:snapshotId/events"
    Registries = "snapshots/:snapshotId/registries"
    RegistryFragments = "snapshots/:snapshotId/registries/:registryId/fragments"

    def __str__(self):
        prefix = getenv("ENV")
        return f"{prefix}_{self.value}" if prefix else self.value


Root = "TWnYURxLxWSNtBOI3Y2936kPyrg1"


class DocumentPaths(str, Enum):
    Lands = "lands/:city/administrativeDistricts/:administrativeDistrict/sections/:section/subsection/:subsection/parentLotNumbers/:parentLotNumber/subLotNumbers/:subLotNumber/years/:year"

    def __str__(self):
        return self.value

# gpt-3.5-turbo: 16385
# gpt-4-turbo: 128000


LanguageModel = "gpt-3.5-turbo"
LanguageModelInputTokensLimit = 16385
