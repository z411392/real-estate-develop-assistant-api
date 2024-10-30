from dataclasses import dataclass
from firebase_admin.auth import UserRecord


@dataclass
class User:
    id: str
    displayName: str
    photoURL: str
    createdAt: int
    updatedAt: int

    @staticmethod
    def from_dict(data: dict):
        _id = str(data.get("id"))
        _displayName = str(data.get("displayName"))
        _photoURL = str(data.get("photoURL"))
        _createdAt = int(data.get("createdAt")) if data.get("createdAt") else None
        _updatedAt = int(data.get("updatedAt")) if data.get("updatedAt") else None
        return User(
            _id,
            _displayName,
            _photoURL,
            _createdAt,
            _updatedAt,
        )

    @staticmethod
    def fromUserRecord(userRecord: UserRecord):
        return User(
            id=userRecord.uid,
            photoURL=userRecord.photo_url,
            displayName=userRecord.display_name,
            createdAt=userRecord.user_metadata.creation_timestamp,
            updatedAt=userRecord.user_metadata.last_refresh_timestamp,
        )
