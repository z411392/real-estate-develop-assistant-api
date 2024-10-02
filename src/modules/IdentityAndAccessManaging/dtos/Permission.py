from dataclasses import dataclass
from src.modules.IdentityAndAccessManaging.dtos.PermissionStatuses import PermissionStatuses
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
