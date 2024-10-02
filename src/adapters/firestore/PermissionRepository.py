from google.cloud.firestore import (
    AsyncClient,
    AsyncTransaction,
    DocumentSnapshot,
)
from src.constants import Collections
from uuid import uuid5, UUID
from src.modules.IdentityAndAccessManaging.dtos.Permission import Permission


class PermissionRepository:
    _db: AsyncClient
    _transaction: AsyncTransaction

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._db = db
        self._transaction = transaction

    def _collection(self):
        return self._db.collection(str(Collections.Permissions))

    @staticmethod
    def nextId(tenantId: str, userId: str):
        return str(uuid5(UUID(tenantId), userId))

    async def get(self, permissionId: str):
        documentSnapshot: DocumentSnapshot = (
            await self._collection()
            .document(permissionId)
            .get(transaction=self._transaction)
        )
        return (
            Permission.fromDocumentSnapshot(documentSnapshot)
            if documentSnapshot.exists
            else None
        )

    async def set(self, permissionId: str, permission: Permission):
        documentReference = self._collection().document(permissionId)
        documentData = permission.copy()
        if documentData.get("id"):
            del documentData["id"]
        if documentData.get("createdAt"):
            del documentData["createdAt"]
        if documentData.get("updatedAt"):
            del documentData["updatedAt"]
        self._transaction.set(documentReference, documentData, merge=True)
