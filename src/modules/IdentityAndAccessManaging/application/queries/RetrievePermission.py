from src.adapters.firestore.PermissionDao import PermissionDao
from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient


class RetrievePermission:
    _logger: Logger
    _permissionDao: PermissionDao

    def __init__(self, db: AsyncClient):
        self._logger = createLogger(__name__)
        self._permissionDao = PermissionDao(db=db)

    async def __call__(self, userId: str, tenantId: str, permissionId):
        permission = await self._permissionDao.byId(permissionId)
        return permission
