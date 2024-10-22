from google.cloud.firestore import AsyncClient, AsyncCollectionReference, AsyncTransaction, DocumentSnapshot
from src.constants import Collections
from uuid import uuid5, UUID
from src.modules.IdentityAndAccessManaging.dtos.Permission import Permission
from dataclasses import asdict


class PermissionRepository:
    _collection: AsyncCollectionReference
    _transaction: AsyncTransaction

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._collection = db.collection(str(Collections.Permissions))
        self._transaction = transaction

    @staticmethod
    def nextId(tenantId: str, userId: str):
        return str(uuid5(UUID(tenantId), userId))

    async def get(self, permissionId: str):
        documentSnapshots: DocumentSnapshot = await self._collection.document(permissionId).get(transaction=self._transaction)
        return Permission.fromDocumentSnapshot(documentSnapshots) if documentSnapshots.exists else None

    async def set(self, permissionId: str, permission: Permission):
        documentReference = self._collection.document(permissionId)
        documentData = asdict(permission)
        del documentData["id"]
        del documentData["createdAt"]
        del documentData["updatedAt"]
        self._transaction.set(documentReference, documentData, merge=True)
