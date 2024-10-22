from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient, AsyncTransaction
from src.adapters.firestore.PermissionRepository import PermissionRepository
from src.modules.TenantManaging.dtos.ReviewingTenantJoining import (
    ReviewingTenantJoining,
)
from src.modules.IdentityAndAccessManaging.errors.PermissionDenied import (
    PermissionDenied,
)
from src.modules.IdentityAndAccessManaging.dtos.Roles import Roles


class ReviewTenantJoining:
    _logger: Logger
    _permissionRepository: PermissionRepository

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._logger = createLogger(__name__)
        self._permissionRepository = PermissionRepository(
            db=db, transaction=transaction
        )

    async def __call__(
        self, userId: str, tenantId: str, mutation: ReviewingTenantJoining
    ):
        permission = await self._permissionRepository.get(mutation.permissionId)
        if not permission:
            raise PermissionDenied()
        if permission.tenantId != tenantId:
            raise PermissionDenied()
        if permission.role != Roles.Member:
            raise PermissionDenied()
        permission.status = mutation.status
        await self._permissionRepository.set(mutation.permissionId, permission)
        return permission.id
