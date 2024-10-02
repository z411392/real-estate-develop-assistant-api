from google.cloud.firestore import (
    AsyncClient,
    AsyncTransaction,
    DocumentSnapshot,
)
from src.constants import Collections
from uuid import uuid5, UUID
from src.modules.RegistryManaging.dtos.Registry import Registry


class RegistryRepository:
    _db: AsyncClient
    _transaction: AsyncTransaction

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._db = db
        self._transaction = transaction

    def _collection(self, snapshotId: str):
        return self._db.collection(
            str(Collections.Registries).replace(":snapshotId", snapshotId)
        )

    @staticmethod
    def nextId(
        snapshotId: str,
        index: int,
    ):
        return str(uuid5(UUID(snapshotId), str(index)))

    async def get(self, snapshotId: str, registryId: str):
        collection = self._collection(snapshotId)
        documentSnapshot: DocumentSnapshot = await collection.document(registryId).get(
            transaction=self._transaction
        )
        return (
            Registry.fromDocumentSnapshot(documentSnapshot)
            if documentSnapshot.exists
            else None
        )

    async def set(self, snapshotId: str, registryId: str, registry: Registry):
        collection = self._collection(snapshotId)
        documentReference = collection.document(registryId)
        documentData = registry.copy()
        if documentData.get("id"):
            del documentData["id"]
        if documentData.get("createdAt"):
            del documentData["createdAt"]
        if documentData.get("updatedAt"):
            del documentData["updatedAt"]
        self._transaction.set(documentReference, documentData, merge=True)
