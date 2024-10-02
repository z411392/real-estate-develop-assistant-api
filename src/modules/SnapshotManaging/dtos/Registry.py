from dataclasses import dataclass
from typing import Any, Optional
from src.modules.SnapshotManaging.dtos.RegistryStatuses import RegistryStatuses
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes


@dataclass
class Registry:
    id: str
    snapshotId: str
    type: SnapshotTypes
    index: int
    status: RegistryStatuses
    text: str
    metadata: Any
    createdAt: Optional[int]
    updatedAt: Optional[int]
