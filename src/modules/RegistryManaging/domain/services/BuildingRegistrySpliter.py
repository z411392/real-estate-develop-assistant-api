from src.modules.RegistryManaging.domain.services.RegistrySpliter import RegistrySpliter
from typing import Optional


class BuildingRegistrySpliter(RegistrySpliter):
    def _parse(self, title: Optional[str], content: str):
        if title is None:
            yield title, 0, content
        else:
            for index, record in self._split(content):
                yield title, index, record
