from dataclasses import dataclass
from src.modules.IdentityAndAccessManaging.dtos.OwnerTypes import OwnerTypes
from src.constants import Collections
from typing import Optional


@dataclass
class Ownership:
    id: str
    ownerId: str
    ownerType: OwnerTypes
    resourceId: str
    resourceType: Collections
    createdAt: Optional[int]
    updatedAt: Optional[int]

    @staticmethod
    def from_dict(obj: dict) -> "Ownership":
        _id = str(obj.get("id"))
        _ownerId = str(obj.get("ownerId"))
        _ownerType = str(obj.get("ownerType"))
        _resourceId = str(obj.get("resourceId"))
        _resourceType = str(obj.get("resourceType"))
        _createdAt = int(obj.get("createdAt")) if obj.get("createdAt") else None
        _updatedAt = int(obj.get("updatedAt")) if obj.get("updatedAt") else None
        return Ownership(
            _id,
            _ownerId,
            _ownerType,
            _resourceId,
            _resourceType,
            _createdAt,
            _updatedAt,
        )
