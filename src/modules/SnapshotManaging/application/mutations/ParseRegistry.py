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
from src.modules.SnapshotManaging.dtos.BuildingRegistry import BuildingRegistry
from src.adapters.db.RealtimeDatabaseDao import RealtimeDatabaseDao
from src.modules.SnapshotManaging.dtos.LandRegistry import LandRegistry
from src.adapters.firestore.TenantRepository import TenantRepository
from src.modules.TenantManaging.dtos.Tenant import Tenant
from src.modules.SnapshotManaging.errors.OutOfCredits import OutOfCredits


class ParseRegistry:
    _logger: Logger
    _registryRepository: RegistryRepository
    _snapshotDao: SnapshotDao
    _openAIService: OpenAIService
    _realtimeDatabaseDao: RealtimeDatabaseDao
    _tenantRepository: TenantRepository

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._logger = createLogger(__name__)
        self._registryRepository = RegistryRepository(db=db, transaction=transaction)
        self._snapshotDao = SnapshotDao(db=db)
        self._openAIService = OpenAIService(apiKey=getenv("OPENAI_API_KEY"))
        self._realtimeDatabaseDao = RealtimeDatabaseDao()
        self._tenantRepository = TenantRepository(db=db, transaction=transaction)

    async def _parseBuildingRegistry(self, registryId: str, registry: Registry):
        if registry.metadata is not None:
            registry.metadata = BuildingRegistry(**registry.metadata)
        if (
            registry.status == RegistryStatuses.Pending or registry.status == RegistryStatuses.Failed
        ):
            registry.status = RegistryStatuses.Doing
            registry.metadata = None
            await self._registryRepository.set(registryId, registry)
            try:
                registry.status = RegistryStatuses.Done
                registry.metadata = await self._openAIService.parseBuildingRegistry(
                    registry.text
                )
            except Exception:
                registry.status = RegistryStatuses.Failed
            await self._registryRepository.set(registryId, registry)
        if registry.metadata is not None:
            metadata: BuildingRegistry = registry.metadata
            await self._realtimeDatabaseDao.touchBuildingRegistry(registryId, metadata)
        return registry

    async def _parseLandRegistry(self, registryId: str, registry: Registry):
        if registry.metadata is not None:
            registry.metadata = LandRegistry(**registry.metadata)
        if (
            registry.status == RegistryStatuses.Pending or registry.status == RegistryStatuses.Failed
        ):
            registry.status = RegistryStatuses.Doing
            registry.metadata = None
            await self._registryRepository.set(registryId, registry)
            try:
                registry.status = RegistryStatuses.Done
                registry.metadata = await self._openAIService.parseLandRegistry(
                    registry.text
                )
            except Exception:
                registry.status = RegistryStatuses.Failed
            await self._registryRepository.set(registryId, registry)
        if registry.metadata is not None:
            metadata: LandRegistry = registry.metadata
            await self._realtimeDatabaseDao.touchLandRegistry(registryId, metadata)
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

        registry = Registry(
            **registrySnapshot.to_dict(),
            id=registrySnapshot.id,
            createdAt=None,
            updatedAt=None
        )
        tenantSnapshot = await self._tenantRepository.get(tenantId)
        tenant = Tenant(
            **tenantSnapshot.to_dict(), id=tenantId, createdAt=None, updatedAt=None
        )
        change = 0
        if tenant.credits <= 0:
            raise OutOfCredits()
        if snapshot.type == SnapshotTypes.Building:
            registry = await self._parseBuildingRegistry(registryId, registry)
            change -= 1
        if snapshot.type == SnapshotTypes.Land:
            registry = await self._parseLandRegistry(registryId, registry)
            change -= 1
        if change != 0:
            tenant.credits += change
            await self._tenantRepository.set(tenantId, tenant)
        return registry
