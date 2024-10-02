from google.cloud.firestore import AsyncClient, AsyncCollectionReference, AsyncTransaction, DocumentSnapshot
from src.constants import Collections
from uuid import uuid5, UUID
from dataclasses import asdict
from src.modules.SnapshotManaging.dtos.Snapshot import Snapshot
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes
from os import getenv


class SnapshotRepository:
    _collection: AsyncCollectionReference
    _transaction: AsyncTransaction

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._collection = db.collection(str(Collections.Snapshots))
        self._transaction = transaction

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
        documentSnapshots: DocumentSnapshot = await self._collection.document(snapshotId).get()
        return documentSnapshots

    async def set(self, snapshotId: str, snapshot: Snapshot):
        documentReference = self._collection.document(snapshotId)
        documentData = asdict(snapshot)
        del documentData["id"]
        del documentData["createdAt"]
        del documentData["updatedAt"]
        self._transaction.set(documentReference, documentData, merge=True)
