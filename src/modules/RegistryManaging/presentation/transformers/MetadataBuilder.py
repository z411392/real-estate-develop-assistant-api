from typing import Optional, List
from src.modules.RegistryFragmentManaging.dtos.RegistryFragment import RegistryFragment
from src.modules.RegistryFragmentManaging.dtos.RegistryFragmentParts import (
    RegistryFragmentParts,
)
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes


class MetadataBuilder:
    _type: SnapshotTypes
    _基本資訊: Optional[dict]
    _標示部: List[dict]
    _所有權部: List[dict]
    _他項權利部: List[dict]

    def __init__(self, type: SnapshotTypes):
        self._type = type
        self._基本資訊 = None
        self._標示部 = []
        self._所有權部 = []
        self._他項權利部 = []

    def __call__(self, fragment: RegistryFragment):
        if fragment.get("part") == RegistryFragmentParts.基本資訊:
            self._基本資訊 = fragment.get("data")
        elif fragment.get("part") == RegistryFragmentParts.標示部:
            self._標示部.append(fragment.get("data"))
        elif fragment.get("part") == RegistryFragmentParts.所有權部:
            self._所有權部.append(fragment.get("data"))
        elif fragment.get("part") == RegistryFragmentParts.他項權利部:
            self._他項權利部.append(fragment.get("data"))

    def accumulated(self):
        if self._基本資訊 is None:
            return None
        if self._type == SnapshotTypes.Building:
            return dict(
                **self._基本資訊,
                建物標示部=self._標示部,
                建物所有權部=self._所有權部,
                建物他項權利部=self._他項權利部,
            )
        elif self._type == SnapshotTypes.Land:
            return dict(
                **self._基本資訊,
                土地標示部=self._標示部,
                土地所有權部=self._所有權部,
                土地他項權利部=self._他項權利部,
            )
        return None
