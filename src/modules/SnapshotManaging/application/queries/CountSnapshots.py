from src.adapters.firestore.OwnershipDao import OwnershipDao
from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient


class CountSnapshots:
    _logger: Logger
    _ownershipDao: OwnershipDao

    def __init__(self, db: AsyncClient):
        self._logger = createLogger(__name__)
        self._ownershipDao = OwnershipDao(db=db)

    async def __call__(self, userId: str, tenantId: str):
        count = await self._ownershipDao.snapshotsAvailableCount(tenantId)
        return count
