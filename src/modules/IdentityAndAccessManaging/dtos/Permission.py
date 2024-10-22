from dataclasses import dataclass
from src.modules.IdentityAndAccessManaging.dtos.PermissionStatuses import (
    PermissionStatuses,
)
from src.modules.IdentityAndAccessManaging.dtos.Roles import Roles
from typing import Optional


@dataclass
class Permission:
    id: str
    tenantId: str
    userId: str
    status: PermissionStatuses
    role: Roles
    createdAt: Optional[int]
    updatedAt: Optional[int]

    @staticmethod
    def from_dict(obj: dict) -> "Permission":
        _id = str(obj.get("id"))
        _tenantId = str(obj.get("tenantId"))
        _userId = str(obj.get("userId"))
        _status = str(obj.get("status"))
        _role = str(obj.get("role"))
        _createdAt = int(obj.get("createdAt")) if obj.get("createdAt") else None
        _updatedAt = int(obj.get("updatedAt")) if obj.get("updatedAt") else None
        return Permission(
            _id,
            _tenantId,
            _userId,
            _status,
            _role,
            _createdAt,
            _updatedAt,
        )
