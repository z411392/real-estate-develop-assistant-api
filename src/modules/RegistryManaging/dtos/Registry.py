from typing import Optional, TypedDict
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes
from google.cloud.firestore import DocumentSnapshot
from datetime import datetime


class Registry(TypedDict):
    id: str
    type: SnapshotTypes
    index: int
    createdAt: Optional[int]
    updatedAt: Optional[int]

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
