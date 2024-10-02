from logging import Logger
from src.utils.development import createLogger
from google.cloud.firestore import AsyncClient
from src.adapters.firestore.TenantDao import TenantDao


class ResolveTenant:
    _logger: Logger
    _tenantDao: TenantDao

    def __init__(self, db: AsyncClient):
        self._logger = createLogger(__name__)
        self._tenantDao = TenantDao(db=db)

    async def __call__(self, userId: str, tenantId: str):
        tenant = await self._tenantDao.byId(tenantId)
        return tenant
