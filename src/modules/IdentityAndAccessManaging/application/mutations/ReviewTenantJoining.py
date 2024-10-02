from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient, AsyncTransaction
from src.adapters.firestore.PermissionRepository import PermissionRepository
from src.modules.IdentityAndAccessManaging.errors.PermissionDenied import (
    PermissionDenied,
)
from src.modules.IdentityAndAccessManaging.dtos.Roles import Roles
from typing import TypedDict
from operator import itemgetter


class ReviewingTenantJoining(TypedDict):
    permissionId: str
    status: str


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
        permissionId, status = itemgetter("permissionId", "status")(mutation)
        permission = await self._permissionRepository.get(permissionId)
        if permission is None:
            raise PermissionDenied()
        if permission.get("tenantId") != tenantId:
            raise PermissionDenied()
        if permission.get("role") != Roles.Member:
            raise PermissionDenied()
        permission["status"] = status
        await self._permissionRepository.set(permissionId, permission)
        return permission.get("id")
