from google.cloud.firestore import AsyncClient, AsyncCollectionReference, FieldFilter
from google.cloud.firestore_v1.field_path import FieldPath
from src.constants import Collections
from typing import List, Mapping, Optional
from src.modules.TenantManaging.dtos.Tenant import Tenant


class TenantDao:
    _collection: AsyncCollectionReference

    def __init__(self, db: AsyncClient):
        self._collection = db.collection(str(Collections.Tenants))

    async def byId(self, tenantId: str):
        tenant: Optional[Tenant] = None
        async for found in self.inIds(tenantId):
            tenant = found
            break
        return tenant

    async def inIds(self, *tenantIds: List[str]):
        stream = self._collection\
            .where(filter=FieldFilter(FieldPath.document_id(), "in", [self._collection.document(tenantId) for tenantId in tenantIds]))\
            .stream()
        mapping: Mapping[str, Tenant] = {}
        async for documentSnapshot in stream:
            mapping[documentSnapshot.id] = Tenant.fromDocumentSnapshot(documentSnapshot)
        for tenantId in tenantIds:
            tenant: Optional[Tenant] = mapping.get(tenantId)
            if tenant is None:
                continue
            yield tenant
