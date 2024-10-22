from firebase_admin.auth import get_users, UidIdentifier, GetUsersResult, UserRecord
from typing import List, Optional
from src.modules.IdentityAndAccessManaging.dtos.User import User
from src.utils.threads import ThreadPoolExecutor


class UserDao:

    def _inIds(self, *userIds: List[str]):
        identifiers = list(map(UidIdentifier, userIds))
        result: GetUsersResult = get_users(identifiers=identifiers)
        users: List[UserRecord] = list(result.users)
        return users

    async def inIds(self, *userIds: List[str]):
        batchSize = 100
        async with ThreadPoolExecutor() as execute:
            for index in range(0, len(userIds), batchSize):
                users: List[UserRecord] = await execute(
                    self._inIds, *userIds[index: index + batchSize]
                )
                for user in users:
                    yield User(
                        id=user.uid,
                        photoURL=user.photo_url,
                        displayName=user.display_name,
                        createdAt=user.user_metadata.creation_timestamp,
                        updatedAt=user.user_metadata.last_refresh_timestamp,
                    )

    async def byId(self, userId: str):
        user: Optional[UserRecord] = None
        async for found in self.inIds(userId):
            user = found
            break
        return user
