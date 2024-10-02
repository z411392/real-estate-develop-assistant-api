from src.adapters.firestore.PermissionDao import PermissionDao
from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient
from src.adapters.auth.UserDao import UserDao
from src.modules.IdentityAndAccessManaging.application.queries.CountUsers import (
    CountingUsers,
)


class ListingUsers(CountingUsers):
    page: int


class ListUsers:
    _logger: Logger
    _permissionDao: PermissionDao
    _userDao: UserDao

    def __init__(self, db: AsyncClient):
        self._logger = createLogger(__name__)
        self._permissionDao = PermissionDao(db=db)
        self._userDao = UserDao()

    async def __call__(self, userId: str, tenantId: str, query: ListingUsers):
        permissionsMap = await self._permissionDao.underTenant(tenantId, query.get("page"))
        if len(permissionsMap) == 0:
            return
        async for user in self._userDao.inIds(*permissionsMap.keys()):
            permission = permissionsMap[user.get("id")]
            yield user, permission
