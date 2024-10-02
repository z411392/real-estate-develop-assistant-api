from typing import Optional, TypedDict
from google.cloud.firestore import DocumentSnapshot
from datetime import datetime


class Tenant(TypedDict):
    id: str
    name: str
    credits: int
    createdAt: Optional[int]
    updatedAt: Optional[int]

    @staticmethod
    def fromDocumentSnapshot(documentSnapshot: DocumentSnapshot):
        createTime: datetime = documentSnapshot.create_time
        createdAt = int(createTime.timestamp() * 1000)
        updateTime: datetime = documentSnapshot.update_time
        updatedAt = int(updateTime.timestamp() * 1000)
        return Tenant(
            **documentSnapshot.to_dict(),
            id=documentSnapshot.id,
            createdAt=createdAt,
            updatedAt=updatedAt
        )
