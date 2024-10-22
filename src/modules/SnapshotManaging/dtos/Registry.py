from dataclasses import dataclass
from typing import Any, Optional
from src.modules.SnapshotManaging.dtos.RegistryStatuses import RegistryStatuses
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes


@dataclass
class Registry:
    id: str
    snapshotId: str
    type: SnapshotTypes
    index: int
    status: RegistryStatuses
    text: str
    metadata: Any
    createdAt: Optional[int]
    updatedAt: Optional[int]

    @staticmethod
    def from_dict(obj: dict) -> "Registry":
        _id = str(obj.get("id"))
        _snapshotId = str(obj.get("snapshotId"))
        _type = str(obj.get("type"))
        _index = int(obj.get("index"))
        _status = str(obj.get("status"))
        _text = str(obj.get("text"))
        _metadata = obj.get("metadata")
        _createdAt = int(obj.get("createdAt")) if obj.get("createdAt") else None
        _updatedAt = int(obj.get("updatedAt")) if obj.get("updatedAt") else None
        return Registry(
            _id,
            _snapshotId,
            _type,
            _index,
            _status,
            _text,
            _metadata,
            _createdAt,
            _updatedAt,
        )
