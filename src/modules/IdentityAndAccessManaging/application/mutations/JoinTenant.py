from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient, AsyncTransaction
from src.adapters.firestore.PermissionRepository import PermissionRepository
from src.modules.IdentityAndAccessManaging.dtos.Permission import Permission
from src.modules.IdentityAndAccessManaging.dtos.Roles import Roles
from src.modules.IdentityAndAccessManaging.dtos.PermissionStatuses import (
    PermissionStatuses,
)
from src.modules.IdentityAndAccessManaging.errors.JoinRequestRejected import (
    JoinRequestRejected,
)
from src.modules.IdentityAndAccessManaging.errors.JoinRequestAlreadySubmitted import (
    JoinRequestAlreadySubmitted,
)
from src.modules.IdentityAndAccessManaging.errors.HasJoinedTenant import HasJoinedTenant


class JoinTenant:
    _logger: Logger
    _permissionRepository: PermissionRepository

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._logger = createLogger(__name__)
        self._permissionRepository = PermissionRepository(
            db=db, transaction=transaction
        )

    async def __call__(
        self,
        userId: str,
        tenantId: str,
    ):
        permissionId = PermissionRepository.nextId(tenantId=tenantId, userId=userId)
        permissionExists = await self._permissionRepository.get(permissionId)
        if permissionExists:
            if permissionExists["status"] == PermissionStatuses.Rejected:
                raise JoinRequestRejected(userId=userId, tenantId=tenantId)
            elif permissionExists["status"] == PermissionStatuses.Pending:
                raise JoinRequestAlreadySubmitted(userId=userId, tenantId=tenantId)
            else:
                raise HasJoinedTenant(userId=userId, tenantId=tenantId)
        permission = Permission(
            dict(
                userId=userId,
                tenantId=tenantId,
                role=Roles.Member,
                status=PermissionStatuses.Pending,
                id=permissionId,
            )
        )
        await self._permissionRepository.set(
            permissionId=permissionId, permission=permission
        )
        return permissionId
