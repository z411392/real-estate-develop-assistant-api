from enum import Enum


class RegistryFragmentParts(str, Enum):
    基本資訊 = "基本資訊"
    標示部 = "標示部"
    所有權部 = "所有權部"
    他項權利部 = "他項權利部"

    def __str__(self):
        return self.value
