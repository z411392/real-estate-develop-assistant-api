from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient, AsyncTransaction
from src.adapters.firestore.RegistryRepository import RegistryRepository
from src.modules.SnapshotManaging.errors.RegistryNotFound import RegistryNotFound
from src.modules.SnapshotManaging.dtos.Registry import Registry
from src.modules.SnapshotManaging.dtos.RegistryStatuses import RegistryStatuses
from src.adapters.firestore.SnapshotDao import SnapshotDao
from src.modules.SnapshotManaging.errors.SnapshotNotFound import SnapshotNotFound
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes
from src.adapters.http.OpenAIService import OpenAIService
from os import getenv
from firebase_admin import db
from src.modules.SnapshotManaging.dtos.BuildingRegistry import BuildingRegistry
from typing import Optional
from src.adapters.db.RealtimeDatabaseDao import RealtimeDatabaseDao


class ParseRegistry:
    _logger: Logger
    _registryRepository: RegistryRepository
    _snapshotDao: SnapshotDao
    _openAIService: OpenAIService
    _realtimeDatabaseDao: RealtimeDatabaseDao

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._logger = createLogger(__name__)
        self._registryRepository = RegistryRepository(db=db, transaction=transaction)
        self._snapshotDao = SnapshotDao(db=db)
        self._openAIService = OpenAIService(apiKey=getenv("OPENAI_API_KEY"))
        self._realtimeDatabaseDao = RealtimeDatabaseDao()

    async def _touchBuildingRegistry(self, metadata: BuildingRegistry):
        ref = db.reference(f"建物/{metadata.謄本核發機關}/{metadata.行政區}/{metadata.地段}/{metadata.小段}/{metadata.建號}")
        record: Optional[dict] = ref.get()
        renewing = True
        if record is not None:
            updatedAt, registryId = next(iter(record.items()))
            renewing = int(updatedAt) < metadata.列印時間
        if renewing:
            ref.set({metadata.列印時間: registryId})

    async def _parseBuildingRegistry(self, registryId: str, registry: Registry):
        if registry.metadata is not None:
            registry.metadata = BuildingRegistry(**registry.metadata)
        if registry.status == RegistryStatuses.Pending or registry.status == RegistryStatuses.Failed:
            registry.status = RegistryStatuses.Doing
            registry.metadata = None
            await self._registryRepository.set(registryId, registry)
            try:
                registry.status = RegistryStatuses.Done
                registry.metadata = await self._openAIService.parseBuildingRegistry(registry.text)
            except Exception:
                registry.status = RegistryStatuses.Failed
            await self._registryRepository.set(registryId, registry)
        if registry.metadata is not None:
            metadata: BuildingRegistry = registry.metadata
            await self._realtimeDatabaseDao.touchBuildingRegistry(registryId, metadata)
        return registry

    async def __call__(
        self,
        userId: str,
        tenantId: str,
        snapshotId: str,
        registryId: str,
    ):
        snapshot = await self._snapshotDao.byId(snapshotId)
        if snapshot is None:
            raise SnapshotNotFound()
        registrySnapshot = await self._registryRepository.get(registryId)
        if not registrySnapshot.exists:
            raise RegistryNotFound()
        registry = Registry(**registrySnapshot.to_dict(), id=registrySnapshot.id, createdAt=None, updatedAt=None)
        if snapshot.type == SnapshotTypes.Buildings:
            registry = await self._parseBuildingRegistry(registryId, registry)
        return registry
