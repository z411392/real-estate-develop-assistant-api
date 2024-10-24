from dataclasses import dataclass, field
from typing import Optional
from google.cloud.firestore import DocumentSnapshot
from datetime import datetime


@dataclass
class Tenant:
    id: str
    name: str
    credits: int
    createdAt: Optional[int] = field(default_factory=lambda: None)
    updatedAt: Optional[int] = field(default_factory=lambda: None)

    @staticmethod
    def from_dict(data: dict):
        return Tenant(
            id=str(data.get("id")),
            name=str(data.get("name")),
            credits=int(data.get("credits")),
            createdAt=int(data.get("createdAt")) if data.get("createdAt") else None,
            updatedAt=int(data.get("updatedAt")) if data.get("updatedAt") else None,
        )

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
