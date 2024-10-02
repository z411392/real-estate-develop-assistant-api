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
