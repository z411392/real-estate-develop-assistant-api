from typing import TypedDict
from firebase_admin.auth import UserRecord


class User(TypedDict):
    id: str
    displayName: str
    photoURL: str
    createdAt: int
    updatedAt: int

    @staticmethod
    def fromUserRecord(userRecord: UserRecord):
        return User(
            id=userRecord.uid,
            photoURL=userRecord.photo_url,
            displayName=userRecord.display_name,
            createdAt=userRecord.user_metadata.creation_timestamp,
            updatedAt=userRecord.user_metadata.last_refresh_timestamp,
        )
