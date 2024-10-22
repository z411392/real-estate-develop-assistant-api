from dataclasses import dataclass
from typing import Optional


@dataclass
class Tenant:
    id: str
    name: str
    credits: int
    createdAt: Optional[int]
    updatedAt: Optional[int]

    @staticmethod
    def from_dict(obj: dict) -> "Tenant":
        _id = str(obj.get("id"))
        _name = str(obj.get("name"))
        _credits = int(obj.get("credits"))
        _createdAt = int(obj.get("createdAt")) if obj.get("createdAt") else None
        _updatedAt = int(obj.get("updatedAt")) if obj.get("updatedAt") else None
        return Tenant(
            _id,
            _name,
            _credits,
            _createdAt,
            _updatedAt,
        )
