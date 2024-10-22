from dataclasses import dataclass, field
from typing import Any, Optional
from src.modules.SnapshotManaging.dtos.RegistryStatuses import RegistryStatuses
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes
from google.cloud.firestore import DocumentSnapshot
from datetime import datetime


@dataclass
class Registry:
    id: str
    snapshotId: str
    type: SnapshotTypes
    index: int
    status: RegistryStatuses
    text: str
    metadata: Any
    createdAt: Optional[int] = field(default_factory=lambda: None)
    updatedAt: Optional[int] = field(default_factory=lambda: None)

    @staticmethod
    def from_dict(obj: dict):
        return Registry(
            id=str(obj.get("id")),
            snapshotId=str(obj.get("snapshotId")),
            type=str(obj.get("type")),
            index=int(obj.get("index")),
            status=str(obj.get("status")),
            text=str(obj.get("text")),
            metadata=obj.get("metadata"),
            createdAt=int(obj.get("createdAt")) if obj.get("createdAt") else None,
            updatedAt=int(obj.get("updatedAt")) if obj.get("updatedAt") else None,
        )

    @staticmethod
    def fromDocumentSnapshot(documentSnapshot: DocumentSnapshot):
        createTime: datetime = documentSnapshot.create_time
        createdAt = int(createTime.timestamp() * 1000)
        updateTime: datetime = documentSnapshot.update_time
        updatedAt = int(updateTime.timestamp() * 1000)
        return Registry(
            **documentSnapshot.to_dict(),
            id=documentSnapshot.id,
            createdAt=createdAt,
            updatedAt=updatedAt
        )
