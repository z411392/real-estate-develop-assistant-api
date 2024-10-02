from src.adapters.firestore.SnapshotDao import SnapshotDao
from src.adapters.firestore.OwnershipDao import OwnershipDao
from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient
from src.modules.SnapshotManaging.application.queries.CountSnapshots import CountingSnapshots


class ListingSnapshots(CountingSnapshots):
    page: int


class ListSnapshots:
    _logger: Logger
    _snapshotDao: SnapshotDao
    _ownershipDao: OwnershipDao

    def __init__(self, db: AsyncClient):
        self._logger = createLogger(__name__)
        self._snapshotDao = SnapshotDao(db=db)
        self._ownershipDao = OwnershipDao(db=db)

    async def __call__(self, userId: str, tenantId: str, query: ListingSnapshots):
        snapshotIds = await self._ownershipDao.snapshotsAvailable(tenantId, query.get("page"))
        if len(snapshotIds) == 0:
            return
        async for snapshot in self._snapshotDao.inIds(*snapshotIds):
            yield snapshot
