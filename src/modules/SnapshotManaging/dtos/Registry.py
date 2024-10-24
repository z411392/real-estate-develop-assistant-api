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
    def from_dict(data: dict):
        return Registry(
            id=str(data.get("id")),
            snapshotId=str(data.get("snapshotId")),
            type=str(data.get("type")),
            index=int(data.get("index")),
            status=str(data.get("status")),
            text=str(data.get("text")),
            metadata=data.get("metadata"),
            createdAt=int(data.get("createdAt")) if data.get("createdAt") else None,
            updatedAt=int(data.get("updatedAt")) if data.get("updatedAt") else None,
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
