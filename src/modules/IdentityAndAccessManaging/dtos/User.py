from dataclasses import dataclass


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
