from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient, AsyncTransaction
from src.adapters.firestore.RegistryRepository import RegistryRepository
from src.modules.SnapshotManaging.errors.RegistryNotFound import RegistryNotFound
from src.modules.SnapshotManaging.dtos.RegistryStatuses import RegistryStatuses
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes
from src.adapters.http.OpenAIService import OpenAIService
from os import getenv
from src.modules.SnapshotManaging.dtos.Registry import Registry
from src.modules.SnapshotManaging.dtos.Prompts import Prompts
from src.modules.SnapshotManaging.dtos.BuildingRegistry import BuildingRegistry
from src.modules.SnapshotManaging.dtos.LandRegistry import LandRegistry
from typing import Optional
from src.utils.realtimeDatabase import get, put


class ParseRegistry:
    _logger: Logger
    _openAIService: OpenAIService
    _registryRepository: RegistryRepository

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._logger = createLogger(__name__)
        self._registryRepository = RegistryRepository(db=db, transaction=transaction)
        self._openAIService = OpenAIService(apiKey=getenv("OPENAI_API_KEY"))

    async def _touchBuildingRegistry(self, registryId: str, metadata: BuildingRegistry):
        key = f"建物/{metadata.謄本核發機關}/{metadata.行政區}/{metadata.地段}/{metadata.小段}/{metadata.建號}"
        record: Optional[dict] = await get(key)
        renewing = False
        if record is not None:
            updatedAt, registryId = next(iter(record.items()))
            renewing = int(updatedAt) >= metadata.列印時間
        if renewing:
            await put(key, {metadata.列印時間: registryId})

    async def _touchLandRegistry(self, registryId: str, metadata: LandRegistry):
        key = f"土地/{metadata.謄本核發機關}/{metadata.行政區}/{metadata.地段}/{metadata.小段}/{metadata.地號}"
        record: Optional[dict] = await get(key)
        renewing = False
        if record is not None:
            updatedAt, registryId = next(iter(record.items()))
            renewing = int(updatedAt) >= metadata.列印時間
        if renewing:
            await put(key, {metadata.列印時間: registryId})

    async def _parseBuildingRegistry(self, registry: Registry):
        try:
            registry.status = RegistryStatuses.Done
            json = await self._openAIService.createCompletion(
                Prompts.BuildingRegistryParsing,
                registry.text,
            )
            registry.metadata = BuildingRegistry(**json)
            await self._registryRepository.set(registry.id, registry)
            await self._touchBuildingRegistry(
                registry.id, registry.metadata
            )
        except Exception:
            registry.status = RegistryStatuses.Failed

    async def _parseLandRegistry(self, registry: Registry):
        try:
            registry.status = RegistryStatuses.Done
            json = await self._openAIService.createCompletion(
                Prompts.LandRegistryParsing,
                registry.text,
            )
            registry.metadata = LandRegistry(**json)
            await self._registryRepository.set(registry.id, registry)
            await self._touchLandRegistry(registry.id, registry.metadata)
        except Exception:
            registry.status = RegistryStatuses.Failed

    async def __call__(
        self,
        userId: str,
        tenantId: str,
        snapshotId: str,
        registryId: str,
    ):
        registry = await self._registryRepository.get(registryId)
        if not registry:
            raise RegistryNotFound()
        if registry.type == SnapshotTypes.Building:
            await self._parseBuildingRegistry(registry)
        elif registry.type == SnapshotTypes.Land:
            await self._parseLandRegistry(registry)
