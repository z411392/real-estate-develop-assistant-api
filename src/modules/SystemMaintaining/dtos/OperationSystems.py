from enum import Enum


class OperationSystems(str, Enum):
    MacOS = "MacOS"
    Linux = "Linux"
    Windows32 = "Windows32"
    Windows64 = "Windows64"
