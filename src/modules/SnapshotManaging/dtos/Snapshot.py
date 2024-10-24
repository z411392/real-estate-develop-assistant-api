from dataclasses import dataclass, field
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes
from typing import Optional
from google.cloud.firestore import DocumentSnapshot
from datetime import datetime


@dataclass
class Snapshot:
    id: str
    name: str
    type: SnapshotTypes
    filePath: str
    userId: str
    createdAt: Optional[int] = field(default_factory=lambda: None)
    updatedAt: Optional[int] = field(default_factory=lambda: None)

    @staticmethod
    def from_dict(data: dict):

        return Snapshot(
            id=str(data.get("id")),
            name=str(data.get("name")),
            type=str(data.get("type")),
            filePath=str(data.get("filePath")),
            userId=str(data.get("userId")),
            createdAt=int(data.get("createdAt")) if data.get("createdAt") else None,
            updatedAt=int(data.get("updatedAt")) if data.get("updatedAt") else None,
        )

    @staticmethod
    def fromDocumentSnapshot(documentSnapshot: DocumentSnapshot):
        createTime: datetime = documentSnapshot.create_time
        createdAt = int(createTime.timestamp() * 1000)
        updateTime: datetime = documentSnapshot.update_time
        updatedAt = int(updateTime.timestamp() * 1000)
        return Snapshot(
            **documentSnapshot.to_dict(),
            id=documentSnapshot.id,
            createdAt=createdAt,
            updatedAt=updatedAt
        )
