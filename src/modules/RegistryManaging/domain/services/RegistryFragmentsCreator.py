from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes
from typing import Optional

from src.utils.calculators import countTokens
from src.modules.RegistryFragmentManaging.dtos.RegistryFragment import RegistryFragment
from src.modules.RegistryFragmentManaging.dtos.RegistryFragmentParts import (
    RegistryFragmentParts,
)
from src.adapters.firestore.RegistryFragmentRepository import RegistryFragmentRepository
from src.modules.RegistryFragmentManaging.dtos.RegistryFragmentStatuses import (
    RegistryFragmentStatuses,
)
from src.modules.RegistryManaging.domain.services.RegistrySpliter import RegistrySpliter
from src.modules.RegistryManaging.domain.services.BuildingRegistrySpliter import (
    BuildingRegistrySpliter,
)
from src.modules.RegistryManaging.domain.services.LandRegistrySpliter import (
    LandRegistrySpliter,
)


class RegistryFragmentsCreator:
    _spliter: Optional[RegistrySpliter] = None

    def __init__(self, type: SnapshotTypes):
        if type == SnapshotTypes.Building:
            self._spliter = BuildingRegistrySpliter()
        if type == SnapshotTypes.Land:
            self._spliter = LandRegistrySpliter()

    def _partOf(self, title: Optional[str]):
        if title is None:
            return RegistryFragmentParts.基本資訊
        if title.find("標示部") > -1:
            return str(RegistryFragmentParts.標示部)
        if title.find("所有權部") > -1:
            return str(RegistryFragmentParts.所有權部)
        if title.find("他項權利部") > -1:
            return str(RegistryFragmentParts.他項權利部)
        return None

    def __call__(self, text: str):
        if self._spliter is None:
            return
        order = -1
        for title, index, text in self._spliter(text):
            part = self._partOf(title)
            if part is None:
                continue
            order += 1
            fragmentId = RegistryFragmentRepository.nextId(
                order=order, part=part, index=index
            )
            fragment = RegistryFragment(
                id=fragmentId,
                part=part,
                index=index,
                text=text,
                tokensCount=countTokens(text),
                status=RegistryFragmentStatuses.Pending,
            )
            yield fragment
