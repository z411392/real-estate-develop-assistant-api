from google.cloud.firestore import AsyncClient, AsyncCollectionReference, FieldFilter
from google.cloud.firestore_v1.field_path import FieldPath
from src.constants import Collections
from typing import List, Mapping, Optional
from src.modules.TenantManaging.dtos.Tenant import Tenant
from datetime import datetime


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
        ids: List[str] = []
        mapping: Mapping[str, Tenant] = {}
        async for document in stream:
            ids.append(document.id)
            createTime: datetime = document.create_time
            createdAt = int(createTime.timestamp() * 1000)
            updateTime: datetime = document.update_time
            updatedAt = int(updateTime.timestamp() * 1000)
            mapping[document.id] = Tenant(**document.to_dict(), id=document.id, createdAt=createdAt, updatedAt=updatedAt)
        for tenantId in tenantIds:
            tenant: Optional[Tenant] = mapping.get(tenantId)
            if tenant is None:
                continue
            yield tenant
