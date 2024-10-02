from google.cloud.firestore import AsyncClient, FieldFilter
from google.cloud.firestore_v1.field_path import FieldPath
from src.constants import Collections
from src.modules.SnapshotManaging.dtos.Snapshot import Snapshot
from typing import List, Mapping, Optional


class SnapshotDao:
    _db: AsyncClient

    def __init__(self, db: AsyncClient):
        self._db = db

    def _collection(self):
        return self._db.collection(str(Collections.Snapshots))

    async def byId(self, snapshotId: str):
        snapshot: Optional[Snapshot] = None
        async for found in self.inIds(snapshotId):
            snapshot = found
            break
        return snapshot

    async def inIds(self, *snapshotIds: List[str]):
        stream = (
            self._collection()
            .where(
                filter=FieldFilter(
                    FieldPath.document_id(),
                    "in",
                    [
                        self._collection().document(snapshotId)
                        for snapshotId in snapshotIds
                    ],
                )
            )
            .stream()
        )
        mapping: Mapping[str, Snapshot] = {}
        async for documentSnapshot in stream:
            mapping[documentSnapshot.id] = Snapshot.fromDocumentSnapshot(
                documentSnapshot
            )
        for snapshotId in snapshotIds:
            snapshot: Optional[Snapshot] = mapping.get(snapshotId)
            if snapshot is None:
                continue
            yield snapshot
