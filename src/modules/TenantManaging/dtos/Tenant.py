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
    def from_dict(obj: dict):
        return Tenant(
            id=str(obj.get("id")),
            name=str(obj.get("name")),
            credits=int(obj.get("credits")),
            createdAt=int(obj.get("createdAt")) if obj.get("createdAt") else None,
            updatedAt=int(obj.get("updatedAt")) if obj.get("updatedAt") else None,
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
