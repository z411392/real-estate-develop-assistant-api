from src.modules.RegistryFragmentManaging.application.mutations.ParseRegistry import (
    ParseRegistry,
)
from src.modules.RegistryFragmentManaging.dtos.RegistryFragment import RegistryFragment
from src.modules.RegistryFragmentManaging.dtos.RegistryFragmentParts import (
    RegistryFragmentParts,
)
from src.modules.RegistryFragmentManaging.errors.InvalidFragment import InvalidFragment
from typing import Optional
from json import loads, dumps


class ParseLandRegistry(ParseRegistry):

    async def _parseFragment(
        self, snapshotId: str, registryId: str, fragment: RegistryFragment
    ):
        cachePath = self._cachePath(snapshotId, registryId, fragment.get("id"))
        hit = await self._loadFromCache(cachePath)
        if hit:
            return loads(hit)
        data: Optional[dict] = None
        if fragment.get("part") == RegistryFragmentParts.基本資訊:
            data = await self._openAIService.解析土地基本資訊(fragment.get("text"))
        elif fragment.get("part") == RegistryFragmentParts.標示部:
            data = await self._openAIService.解析土地標示(fragment.get("text"))
        elif fragment.get("part") == RegistryFragmentParts.所有權部:
            data = await self._openAIService.解析土地所有權(fragment.get("text"))
        elif fragment.get("part") == RegistryFragmentParts.他項權利部:
            data = await self._openAIService.解析土地他項權利(fragment.get("text"))
        if data is None:
            raise InvalidFragment(
                snapshotId=snapshotId,
                registryId=registryId,
                fragmentId=fragment.get("id"),
            )
        await self._saveToCache(cachePath, dumps(data))
        return data
