from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient, AsyncTransaction
from src.adapters.firestore.TenantRepository import TenantRepository
from src.adapters.firestore.TenantDao import TenantDao
from src.adapters.firestore.PermissionRepository import PermissionRepository
from src.modules.TenantManaging.errors.TenantConflict import TenantConflict
from src.adapters.firestore.PermissionDao import PermissionDao
from src.modules.TenantManaging.errors.TenantCreatingInProgress import (
    TenantCreatingInProgress,
)
from src.modules.TenantManaging.dtos.Tenant import Tenant
from src.modules.IdentityAndAccessManaging.dtos.Permission import Permission
from src.modules.IdentityAndAccessManaging.dtos.Roles import Roles
from src.modules.IdentityAndAccessManaging.dtos.PermissionStatuses import (
    PermissionStatuses,
)
from typing import TypedDict
from operator import itemgetter


class CreatingTenant(TypedDict):
    name: str


class CreateTenant:
    _logger: Logger
    _tenantDao: TenantDao
    _tenantRepository: TenantRepository
    _permissionDao: PermissionDao
    _permissionRepository: PermissionRepository

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._logger = createLogger(__name__)
        self._tenantDao = TenantDao(db=db)
        self._tenantRepository = TenantRepository(db=db, transaction=transaction)
        self._permissionDao = PermissionDao(db=db)
        self._permissionRepository = PermissionRepository(
            db=db, transaction=transaction
        )

    async def __call__(self, userId: str, mutation: CreatingTenant):
        name = itemgetter("name")(mutation)
        anotherTenantId = await self._tenantDao.findOne(name=name)
        if anotherTenantId:
            raise TenantConflict(name=name)
        isWaitingForTenantCreation = (
            await self._permissionDao.isWaitingForTenantCreation(userId)
        )
        if isWaitingForTenantCreation:
            raise TenantCreatingInProgress(
                userId=userId,
            )
        tenantId = self._tenantRepository.nextId()
        tenant = Tenant(dict(name=name, id=tenantId, credits=50))
        permissionId = PermissionRepository.nextId(tenantId=tenantId, userId=userId)
        permission = Permission(
            tenantId=tenantId,
            role=Roles.Owner,
            status=PermissionStatuses.Pending,
            userId=userId,
            id=permissionId,
        )
        await self._tenantRepository.set(tenantId, tenant)
        await self._permissionRepository.set(permissionId, permission)
        return tenantId
