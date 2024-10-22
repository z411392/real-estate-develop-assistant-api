from google.cloud.firestore import AsyncClient, AsyncCollectionReference, AsyncTransaction, DocumentSnapshot
from src.constants import Collections
from uuid import uuid5, UUID
from os import getenv
from src.modules.TenantManaging.dtos.Tenant import Tenant
from dataclasses import asdict


class TenantRepository:
    _collection: AsyncCollectionReference
    _transaction: AsyncTransaction

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._collection = db.collection(str(Collections.Tenants))
        self._transaction = transaction

    @staticmethod
    def nextId(name: str):
        projectId = UUID(getenv("PROJECT_UUID"))
        collectionName = str(Collections.Tenants)
        namespace = uuid5(projectId, collectionName)
        return str(uuid5(namespace, name))

    async def get(self, tenantId: str):
        documentSnapshots: DocumentSnapshot = await self._collection.document(tenantId).get(transaction=self._transaction)
        return Tenant.fromDocumentSnapshot(documentSnapshots) if documentSnapshots.exists else None

    async def set(self, tenantId: str, tenant: Tenant):
        documentReference = self._collection.document(tenantId)
        documentData = asdict(tenant)
        del documentData["id"]
        del documentData["createdAt"]
        del documentData["updatedAt"]
        self._transaction.set(documentReference, documentData, merge=True)
