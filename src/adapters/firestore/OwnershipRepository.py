from google.cloud.firestore import (
    AsyncClient,
    AsyncTransaction,
    DocumentSnapshot,
)
from src.constants import Collections
from uuid import uuid5, UUID
from src.modules.IdentityAndAccessManaging.dtos.Ownership import Ownership


class OwnershipRepository:
    _db: AsyncClient
    _transaction: AsyncTransaction

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._db = db
        self._transaction = transaction

    def _collection(self):
        return self._db.collection(str(Collections.Ownerships))

    @staticmethod
    def nextId(
        ownerId: str,
        resourceId: str,
    ):
        return str(uuid5(UUID(ownerId), resourceId))

    async def get(self, ownershipId: str):
        documentSnapshot: DocumentSnapshot = (
            await self._collection()
            .document(ownershipId)
            .get(transaction=self._transaction)
        )
        return (
            Ownership.fromDocumentSnapshot(documentSnapshot)
            if documentSnapshot.exists
            else None
        )

    async def set(self, ownershipId: str, ownership: Ownership):
        documentReference = self._collection().document(ownershipId)
        documentData = ownership.copy()
        if documentData.get("id"):
            del documentData["id"]
        if documentData.get("createdAt"):
            del documentData["createdAt"]
        if documentData.get("updatedAt"):
            del documentData["updatedAt"]
        self._transaction.set(documentReference, documentData, merge=True)
