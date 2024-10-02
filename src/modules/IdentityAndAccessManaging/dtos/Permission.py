from src.modules.IdentityAndAccessManaging.dtos.PermissionStatuses import (
    PermissionStatuses,
)
from src.modules.IdentityAndAccessManaging.dtos.Roles import Roles
from typing import Optional, TypedDict
from google.cloud.firestore import DocumentSnapshot
from datetime import datetime


class Permission(TypedDict):
    id: str
    tenantId: str
    userId: str
    status: PermissionStatuses
    role: Roles
    createdAt: Optional[int]
    updatedAt: Optional[int]

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
