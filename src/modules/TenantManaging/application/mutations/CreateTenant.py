from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient, AsyncTransaction
from src.modules.TenantManaging.dtos.CreatingTenant import CreatingTenant
from src.adapters.firestore.TenantRepository import TenantRepository
from src.adapters.firestore.PermissionRepository import PermissionRepository
from src.modules.TenantManaging.errors.TenantNameConflict import TenantNameConflict
from src.adapters.firestore.PermissionDao import PermissionDao
from src.modules.TenantManaging.errors.TenantCreatingInProgress import TenantCreatingInProgress
from src.modules.TenantManaging.dtos.Tenant import Tenant
from src.modules.IdentityAndAccessManaging.dtos.Permission import Permission
from src.modules.IdentityAndAccessManaging.dtos.Roles import Roles
from src.modules.IdentityAndAccessManaging.dtos.PermissionStatuses import PermissionStatuses


class CreateTenant:
    _logger: Logger
    _tenantRepository: TenantRepository
    _permissionDao: PermissionDao
    _permissionRepository: PermissionRepository

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._logger = createLogger(__name__)
        self._tenantRepository = TenantRepository(
            db=db, transaction=transaction)
        self._permissionDao = PermissionDao(db=db)
        self._permissionRepository = PermissionRepository(
            db=db, transaction=transaction)

    async def __call__(
            self,
            userId: str,
            mutation: CreatingTenant):
        tenantId = self._tenantRepository.nextId(name=mutation.name)
        tenantSnapshot = await self._tenantRepository.get(tenantId)
        if tenantSnapshot.exists:
            raise TenantNameConflict()
        if await self._permissionDao.isWaitingForTenantCreation(userId):
            raise TenantCreatingInProgress()
        tenant = Tenant(name=mutation.name, id=tenantId, createdAt=None, updatedAt=None)
        permissionId = PermissionRepository.nextId(
            tenantId=tenantId, userId=userId)
        permission = Permission(
            tenantId=tenantId,
            role=Roles.Owner,
            status=PermissionStatuses.Pending,
            userId=userId,
            id=permissionId,
            createdAt=None,
            updatedAt=None,
        )
        await self._tenantRepository.set(tenantId, tenant)
        await self._permissionRepository.set(permissionId, permission)
        return tenantId
