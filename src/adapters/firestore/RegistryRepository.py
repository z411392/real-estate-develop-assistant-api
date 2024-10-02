from google.cloud.firestore import AsyncClient, AsyncCollectionReference, AsyncTransaction, DocumentSnapshot
from src.constants import Collections
from uuid import uuid5, UUID
from dataclasses import asdict
from src.modules.SnapshotManaging.dtos.Registry import Registry


class RegistryRepository:
    _collection: AsyncCollectionReference
    _transaction: AsyncTransaction

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._collection = db.collection(str(Collections.Registries))
        self._transaction = transaction

    @staticmethod
    def nextId(
        snapshotId: str,
        index: int,
    ):
        return str(uuid5(UUID(snapshotId), str(index)))

    async def get(self, registryId: str):
        documentSnapshots: DocumentSnapshot = await self._collection.document(registryId).get()
        return documentSnapshots

    async def set(self, registryId: str, registry: Registry):
        documentReference = self._collection.document(registryId)
        documentData = asdict(registry)
        del documentData["id"]
        del documentData["createdAt"]
        del documentData["updatedAt"]
        self._transaction.set(documentReference, documentData, merge=True)
