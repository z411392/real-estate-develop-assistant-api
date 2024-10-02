from src.adapters.firestore.RegistryDao import RegistryDao
from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient
from src.modules.RegistryManaging.application.queries.CountRegistries import (
    CountingRegistries,
)


class ListingRegistries(CountingRegistries):
    pass


class ListRegistries:
    _logger: Logger
    _registryDao: RegistryDao

    def __init__(self, db: AsyncClient):
        self._logger = createLogger(__name__)
        self._registryDao = RegistryDao(db=db)

    async def __call__(self, userId: str, tenantId: str, snapshotId: str, query: ListingRegistries):
        registryIds = await self._registryDao.registriesAvailable(snapshotId)
        if len(registryIds) == 0:
            return
        async for registry in self._registryDao.inIds(snapshotId, *registryIds):
            yield registry
