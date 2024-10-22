from dataclasses import dataclass
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes
from typing import Optional


@dataclass
class Snapshot:
    id: str
    name: str
    type: SnapshotTypes
    filePath: str
    userId: str
    createdAt: Optional[int]
    updatedAt: Optional[int]

    @staticmethod
    def from_dict(obj: dict) -> "Snapshot":
        _id = str(obj.get("id"))
        _name = str(obj.get("name"))
        _type = str(obj.get("type"))
        _filePath = str(obj.get("filePath"))
        _userId = str(obj.get("userId"))
        _createdAt = int(obj.get("createdAt")) if obj.get("createdAt") else None
        _updatedAt = int(obj.get("updatedAt")) if obj.get("updatedAt") else None
        return Snapshot(
            _id,
            _name,
            _type,
            _filePath,
            _userId,
            _createdAt,
            _updatedAt,
        )
