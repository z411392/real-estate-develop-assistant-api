from dataclasses import dataclass, field
from src.modules.IdentityAndAccessManaging.dtos.PermissionStatuses import (
    PermissionStatuses,
)
from src.modules.IdentityAndAccessManaging.dtos.Roles import Roles
from typing import Optional
from google.cloud.firestore import DocumentSnapshot
from datetime import datetime


@dataclass
class Permission:
    id: str
    tenantId: str
    userId: str
    status: PermissionStatuses
    role: Roles
    createdAt: Optional[int] = field(default_factory=lambda: None)
    updatedAt: Optional[int] = field(default_factory=lambda: None)

    @staticmethod
    def from_dict(obj: dict):
        return Permission(
            id=str(obj.get("id")),
            tenantId=str(obj.get("tenantId")),
            userId=str(obj.get("userId")),
            status=str(obj.get("status")),
            role=str(obj.get("role")),
            createdAt=int(obj.get("createdAt")) if obj.get("createdAt") else None,
            updatedAt=int(obj.get("updatedAt")) if obj.get("updatedAt") else None,
        )

    @staticmethod
    def fromDocumentSnapshot(documentSnapshot: DocumentSnapshot):
        createTime: datetime = documentSnapshot.create_time
        createdAt = int(createTime.timestamp() * 1000)
        updateTime: datetime = documentSnapshot.update_time
        updatedAt = int(updateTime.timestamp() * 1000)
        return Permission(
            **documentSnapshot.to_dict(),
            id=documentSnapshot.id,
            createdAt=createdAt,
            updatedAt=updatedAt
        )
