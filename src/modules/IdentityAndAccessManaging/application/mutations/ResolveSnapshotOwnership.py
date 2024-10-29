from logging import Logger
from src.utils.development import createLogger
from google.cloud.firestore import AsyncClient
from src.adapters.firestore.OwnershipDao import OwnershipDao
from src.modules.IdentityAndAccessManaging.dtos.OwnerTypes import OwnerTypes
from src.constants import Collections


class ResolveSnapshotOwnership:
    _logger: Logger
    _ownershipDao: OwnershipDao

    def __init__(self, db: AsyncClient):
        self._logger = createLogger(__name__)
        self._ownershipDao = OwnershipDao(db=db)

    async def __call__(self, userId: str, tenantId: str, snapshotId: str):
        ownership = await self._ownershipDao.findOne(
            ownerType=str(OwnerTypes.Tenant),
            ownerId=tenantId,
            resourceType=str(Collections.Snapshots),
            resourceId=snapshotId,
        )
        return ownership
