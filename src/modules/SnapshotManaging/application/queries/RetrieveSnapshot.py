from src.adapters.firestore.SnapshotDao import SnapshotDao
from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient


class RetrieveSnapshot:
    _logger: Logger
    _snapshotDao: SnapshotDao

    def __init__(self, db: AsyncClient):
        self._logger = createLogger(__name__)
        self._snapshotDao = SnapshotDao(db=db)

    async def __call__(self, userId: str, tenantId: str, snapshotId: str):
        snapshot = await self._snapshotDao.byId(snapshotId)
        return snapshot
