from src.adapters.firestore.TenantDao import TenantDao
from src.adapters.firestore.PermissionDao import PermissionDao
from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient
from src.modules.TenantManaging.application.queries.CountTenants import CountingTenants


class ListingTenants(CountingTenants):
    page: int


class ListTenants:
    _logger: Logger
    _tenantDao: TenantDao
    _permissionDao: PermissionDao

    def __init__(self, db: AsyncClient):
        self._logger = createLogger(__name__)
        self._tenantDao = TenantDao(db=db)
        self._permissionDao = PermissionDao(db=db)

    async def __call__(self, userId: str, query: ListingTenants):
        tenantIds = await self._permissionDao.tenantsAvailable(userId, query.get("page"))
        if len(tenantIds) == 0:
            return
        async for tenant in self._tenantDao.inIds(*tenantIds):
            yield tenant
