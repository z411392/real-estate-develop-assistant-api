from dataclasses import dataclass
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes
from typing import Optional


@dataclass
class Snapshot:
    id: str
    type: SnapshotTypes
    filePath: str
    userId: str
    createdAt: Optional[int]
    updatedAt: Optional[int]
