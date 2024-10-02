from logging import Logger
from src.utils.development import createLogger
from google.cloud.firestore import AsyncClient
from src.adapters.firestore.OwnershipDao import OwnershipDao
from src.adapters.firestore.SnapshotDao import SnapshotDao
from src.adapters.firestore.OwnershipRepository import OwnershipRepository


class ResolveSnapshot:
    _logger: Logger
    _ownershipDao: OwnershipDao
    _snapshotDao: SnapshotDao

    def __init__(self, db: AsyncClient):
        self._logger = createLogger(__name__)
        self._ownershipDao = OwnershipDao(db=db)
        self._snapshotDao = SnapshotDao(db=db)

    async def __call__(self, userId: str, tenantId: str, snapshotId: str):
        ownershipId = OwnershipRepository.nextId(ownerId=tenantId, resourceId=snapshotId)
        ownership = await self._ownershipDao.byId(ownershipId)
        if ownership is None:
            return None
        snapshot = await self._snapshotDao.byId(snapshotId)
        return snapshot
