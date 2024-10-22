from dataclasses import dataclass


@dataclass
class User:
    id: str
    displayName: str
    photoURL: str
    createdAt: int
    updatedAt: int

    @staticmethod
    def from_dict(obj: dict) -> "User":
        _id = str(obj.get("id"))
        _displayName = str(obj.get("displayName"))
        _photoURL = str(obj.get("photoURL"))
        _createdAt = int(obj.get("createdAt")) if obj.get("createdAt") else None
        _updatedAt = int(obj.get("updatedAt")) if obj.get("updatedAt") else None
        return User(
            _id,
            _displayName,
            _photoURL,
            _createdAt,
            _updatedAt,
        )
