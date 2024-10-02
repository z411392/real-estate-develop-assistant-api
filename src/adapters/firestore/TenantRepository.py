from google.cloud.firestore import (
    AsyncClient,
    AsyncTransaction,
    DocumentSnapshot,
)
from src.constants import Collections
from uuid import uuid5, UUID, uuid1
from os import getenv
from src.modules.TenantManaging.dtos.Tenant import Tenant


class TenantRepository:
    _db: AsyncClient
    _transaction: AsyncTransaction

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._db = db
        self._transaction = transaction

    def _collection(self):
        return self._db.collection(str(Collections.Tenants))

    @staticmethod
    def nextId():
        projectId = UUID(getenv("PROJECT_UUID"))
        collectionName = str(Collections.Tenants)
        namespace = uuid5(projectId, collectionName)
        return str(uuid5(namespace, uuid1()))

    async def get(self, tenantId: str):
        documentSnapshot: DocumentSnapshot = (
            await self._collection()
            .document(tenantId)
            .get(transaction=self._transaction)
        )
        return (
            Tenant.fromDocumentSnapshot(documentSnapshot)
            if documentSnapshot.exists
            else None
        )

    async def set(self, tenantId: str, tenant: Tenant):
        documentReference = self._collection().document(tenantId)
        documentData = tenant.copy()
        if documentData.get("id"):
            del documentData["id"]
        if documentData.get("createdAt"):
            del documentData["createdAt"]
        if documentData.get("updatedAt"):
            del documentData["updatedAt"]
        self._transaction.set(documentReference, documentData, merge=True)
