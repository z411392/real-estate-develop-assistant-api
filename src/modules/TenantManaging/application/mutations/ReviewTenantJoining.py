from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient, AsyncTransaction
from src.adapters.firestore.PermissionRepository import PermissionRepository
from src.modules.IdentityAndAccessManaging.dtos.Permission import Permission
from src.modules.TenantManaging.dtos.ReviewingTenantJoining import ReviewingTenantJoining
from src.modules.IdentityAndAccessManaging.errors.PermissionDenied import PermissionDenied
from src.modules.IdentityAndAccessManaging.dtos.PermissionStatuses import PermissionStatuses
from src.modules.IdentityAndAccessManaging.dtos.Roles import Roles


class ReviewTenantJoining:
    _logger: Logger
    _permissionRepository: PermissionRepository

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._logger = createLogger(__name__)
        self._permissionRepository = PermissionRepository(db=db, transaction=transaction)

    async def __call__(
            self,
            userId: str,
            tenantId: str,
            mutation: ReviewingTenantJoining):
        permissionSnapshot = await self._permissionRepository.get(mutation.permissionId)
        if not permissionSnapshot.exists:
            raise PermissionDenied()
        permission = Permission(
            **permissionSnapshot.to_dict(),
            id=permissionSnapshot.id,
            createdAt=None,
            updatedAt=None,
        )
        if permission.tenantId != tenantId:
            raise PermissionDenied()
        if permission.status != PermissionStatuses.Pending:
            raise PermissionDenied()
        if permission.role != Roles.Member:
            raise PermissionDenied()
        permission.status = mutation.status
        await self._permissionRepository.set(permissionId=permission.id, permission=permission)
        return permission.id
