from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes
from typing import List
from src.modules.RegistryFragmentManaging.dtos.RegistryFragment import RegistryFragment
from src.modules.RegistryFragmentManaging.dtos.RegistryFragmentParts import (
    RegistryFragmentParts,
)


class TextComposer:
    _type: SnapshotTypes
    _texts: List[str]

    def __init__(self, type: SnapshotTypes):
        self._type = type
        self._texts = []

    def accumulated(self):
        return "\n".join(self._texts)

    def __call__(self, fragment: RegistryFragment):
        if fragment.get("part") != RegistryFragmentParts.基本資訊:
            if fragment.get("index") == 0:
                prefix = ""
                if self._type == SnapshotTypes.Building:
                    prefix = "建物"
                elif self._type == SnapshotTypes.Land:
                    prefix = "土地"
                self._texts.append(f'\n{prefix}{fragment.get("part")}')
        self._texts.append(fragment.get("text"))
