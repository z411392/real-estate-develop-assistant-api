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
    def from_dict(obj: dict):
        return Ownership(
            id=str(obj.get("id")),
            ownerId=str(obj.get("ownerId")),
            ownerType=str(obj.get("ownerType")),
            resourceId=str(obj.get("resourceId")),
            resourceType=str(obj.get("resourceType")),
            createdAt=int(obj.get("createdAt")) if obj.get("createdAt") else None,
            updatedAt=int(obj.get("updatedAt")) if obj.get("updatedAt") else None,
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
