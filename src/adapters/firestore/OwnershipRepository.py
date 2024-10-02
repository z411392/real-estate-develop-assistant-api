from google.cloud.firestore import AsyncClient, AsyncCollectionReference, AsyncTransaction, DocumentSnapshot
from src.constants import Collections
from uuid import uuid5, UUID
from src.modules.IdentityAndAccessManaging.dtos.Ownership import Ownership
from dataclasses import asdict


class OwnershipRepository:
    _collection: AsyncCollectionReference
    _transaction: AsyncTransaction

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._collection = db.collection(str(Collections.Ownerships))
        self._transaction = transaction

    @staticmethod
    def nextId(
        ownerId: str,
        resourceId: str,
    ):
        return str(uuid5(UUID(ownerId), resourceId))

    async def get(self, ownershipId: str):
        documentSnapshots: DocumentSnapshot = await self._collection.document(ownershipId).get()
        return documentSnapshots

    async def set(self, ownershipId: str, ownership: Ownership):
        documentReference = self._collection.document(ownershipId)
        documentData = asdict(ownership)
        del documentData["id"]
        del documentData["createdAt"]
        del documentData["updatedAt"]
        self._transaction.set(documentReference, documentData, merge=True)
