from dataclasses import dataclass, field
from src.modules.IdentityAndAccessManaging.dtos.OwnerTypes import OwnerTypes
from src.constants import Collections
from typing import Optional
from google.cloud.firestore import DocumentSnapshot
from datetime import datetime


@dataclass
class Ownership:
    id: str
    ownerId: str
    ownerType: OwnerTypes
    resourceId: str
    resourceType: Collections
    createdAt: Optional[int] = field(default_factory=lambda: None)
    updatedAt: Optional[int] = field(default_factory=lambda: None)

    @staticmethod
    def from_dict(data: dict):
        return Ownership(
            id=str(data.get("id")),
            ownerId=str(data.get("ownerId")),
            ownerType=str(data.get("ownerType")),
            resourceId=str(data.get("resourceId")),
            resourceType=str(data.get("resourceType")),
            createdAt=int(data.get("createdAt")) if data.get("createdAt") else None,
            updatedAt=int(data.get("updatedAt")) if data.get("updatedAt") else None,
        )

    @staticmethod
    def fromDocumentSnapshot(documentSnapshot: DocumentSnapshot):
        createTime: datetime = documentSnapshot.create_time
        createdAt = int(createTime.timestamp() * 1000)
        updateTime: datetime = documentSnapshot.update_time
        updatedAt = int(updateTime.timestamp() * 1000)
        return Ownership(
            **documentSnapshot.to_dict(),
            id=documentSnapshot.id,
            createdAt=createdAt,
            updatedAt=updatedAt
        )
