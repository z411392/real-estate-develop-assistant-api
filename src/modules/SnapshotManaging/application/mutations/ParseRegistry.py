from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient, AsyncTransaction
from src.adapters.firestore.RegistryRepository import RegistryRepository
from src.modules.SnapshotManaging.errors.RegistryNotFound import RegistryNotFound
from src.modules.SnapshotManaging.dtos.RegistryStatuses import RegistryStatuses
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes
from src.adapters.http.OpenAIService import OpenAIService
from os import getenv
from src.adapters.db.RealtimeDatabaseDao import RealtimeDatabaseDao
from src.modules.SnapshotManaging.dtos.Registry import Registry
from src.modules.SnapshotManaging.dtos.Prompts import Prompts
from src.modules.SnapshotManaging.dtos.BuildingRegistry import BuildingRegistry
from src.modules.SnapshotManaging.dtos.LandRegistry import LandRegistry


class ParseRegistry:
    _logger: Logger
    _openAIService: OpenAIService
    _realtimeDatabaseDao: RealtimeDatabaseDao
    _registryRepository: RegistryRepository

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._logger = createLogger(__name__)
        self._registryRepository = RegistryRepository(db=db, transaction=transaction)
        self._openAIService = OpenAIService(apiKey=getenv("OPENAI_API_KEY"))
        self._realtimeDatabaseDao = RealtimeDatabaseDao()

    async def _parseBuildingRegistry(self, registry: Registry):
        try:
            registry.status = RegistryStatuses.Done
            json = await self._openAIService.createCompletion(
                Prompts.BuildingRegistryParsing,
                registry.text,
            )
            registry.metadata = BuildingRegistry(**json)
            await self._registryRepository.set(registry.id, registry)
            await self._realtimeDatabaseDao.touchBuildingRegistry(
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
            await self._realtimeDatabaseDao.touchLandRegistry(registry.id, registry.metadata)
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
