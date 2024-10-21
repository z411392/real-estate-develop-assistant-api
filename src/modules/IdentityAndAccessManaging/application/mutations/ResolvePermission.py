from logging import Logger
from src.utils.development import createLogger
from google.cloud.firestore import AsyncClient
from src.adapters.firestore.TenantDao import TenantDao
from src.adapters.firestore.PermissionDao import PermissionDao
from src.adapters.firestore.PermissionRepository import PermissionRepository


class ResolvePermission:
    _logger: Logger
    _tenantDao: TenantDao
    _permissionDao: PermissionDao

    def __init__(self, db: AsyncClient):
        self._logger = createLogger(__name__)
        self._tenantDao = TenantDao(db=db)
        self._permissionDao = PermissionDao(db=db)

    async def __call__(self, userId: str, tenantId: str):
        tenant = await self._tenantDao.byId(tenantId)
        if tenant is None:
            return None
        permissionId = PermissionRepository.nextId(
            tenantId=tenantId, userId=userId)
        permission = await self._permissionDao.byId(permissionId)
        return tenant, permission
