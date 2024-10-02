from dataclasses import dataclass
from typing import Optional


@dataclass
class Tenant:
    id: str
    name: str
    createdAt: Optional[int]
    updatedAt: Optional[int]
