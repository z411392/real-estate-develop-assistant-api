from google.cloud.firestore import AsyncClient, AsyncTransaction, DocumentSnapshot
from src.constants import Collections
from uuid import uuid5, UUID
from src.modules.SnapshotManaging.dtos.Snapshot import Snapshot
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes
from os import getenv


class SnapshotRepository:
    _db: AsyncClient
    _transaction: AsyncTransaction

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._db = db
        self._transaction = transaction

    def _collection(self):
        return self._db.collection(str(Collections.Snapshots))

    @staticmethod
    def nextId(
        snapshotType: SnapshotTypes,
        filePath: str,
    ):
        projectId = UUID(getenv("PROJECT_UUID"))
        collectionName = str(Collections.Snapshots)
        namespace = uuid5(uuid5(projectId, collectionName), snapshotType)
        return str(uuid5(namespace, filePath))

    async def get(self, snapshotId: str):
        documentSnapshot: DocumentSnapshot = (
            await self._collection()
            .document(snapshotId)
            .get(transaction=self._transaction)
        )
        return (
            Snapshot.fromDocumentSnapshot(documentSnapshot)
            if documentSnapshot.exists
            else None
        )

    async def set(self, snapshotId: str, snapshot: Snapshot):
        documentReference = self._collection().document(snapshotId)
        documentData = snapshot.copy()
        if documentData.get("id"):
            del documentData["id"]
        if documentData.get("createdAt"):
            del documentData["createdAt"]
        if documentData.get("updatedAt"):
            del documentData["updatedAt"]
        self._transaction.set(documentReference, documentData, merge=True)
