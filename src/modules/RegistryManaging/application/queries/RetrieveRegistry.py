from src.adapters.firestore.RegistryDao import RegistryDao
from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient


class RetrieveRegistry:
    _logger: Logger
    _registryDao: RegistryDao

    def __init__(self, db: AsyncClient):
        self._logger = createLogger(__name__)
        self._registryDao = RegistryDao(db=db)

    async def __call__(self, userId: str, tenantId: str, snapshotId: str, registryId: str):
        registry = await self._registryDao.byId(snapshotId, registryId)
        return registry
