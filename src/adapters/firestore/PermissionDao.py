from google.cloud.firestore import AsyncClient, FieldFilter
from google.cloud.firestore_v1.field_path import FieldPath
from google.cloud.firestore_v1.async_query import AsyncAggregationQuery
from src.constants import Collections, PageSizes
from src.modules.IdentityAndAccessManaging.dtos.PermissionStatuses import (
    PermissionStatuses,
)
from typing import List, Mapping, Optional
from operator import itemgetter
from src.modules.IdentityAndAccessManaging.dtos.Roles import Roles
from src.modules.IdentityAndAccessManaging.dtos.Permission import Permission


class PermissionDao:
    _db: AsyncClient

    def __init__(self, db: AsyncClient):
        self._db = db

    def _collection(self):
        return self._db.collection(str(Collections.Permissions))

    async def tenantsAvailable(
        self, userId: str, page: int, limit: int = PageSizes.Tenants
    ):
        offset = (page - 1) * limit
        tenantIds: List[str] = []
        stream = (
            self._collection()
            .where(filter=FieldFilter("userId", "==", userId))
            .where(filter=FieldFilter("status", "==", PermissionStatuses.Approved))
            .limit(limit)
            .offset(offset)
            .select(["tenantId"])
            .stream()
        )
        async for documentSnapshot in stream:
            tenantId = itemgetter("tenantId")(documentSnapshot.to_dict())
            tenantIds.append(tenantId)
        return tenantIds

    async def tenantsAvailableCount(self, userId: str):
        query: AsyncAggregationQuery = (
            self._collection()
            .where(filter=FieldFilter("userId", "==", userId))
            .where(filter=FieldFilter("status", "==", PermissionStatuses.Approved))
            .count()
        )
        queryResultsList = await query.get()
        queryResults = next(iter(queryResultsList))
        queryResult = next(iter(queryResults))
        return int(queryResult.value)

    async def isWaitingForTenantCreation(self, userId: str):
        query: AsyncAggregationQuery = (
            self._collection()
            .where(filter=FieldFilter("userId", "==", userId))
            .where(filter=FieldFilter("status", "==", PermissionStatuses.Pending))
            .where(filter=FieldFilter("role", "==", Roles.Owner))
            .count()
        )
        queryResultsList = await query.get()
        queryResults = next(iter(queryResultsList))
        queryResult = next(iter(queryResults))
        return int(queryResult.value) > 0

    async def byId(self, permissionId: str):
        permission: Optional[Permission] = None
        async for found in self.inIds(permissionId):
            permission = found
            break
        return permission

    async def inIds(self, *permissionIds: List[str]):
        stream = (
            self._collection()
            .where(
                filter=FieldFilter(
                    FieldPath.document_id(),
                    "in",
                    [
                        self._collection().document(permissionId)
                        for permissionId in permissionIds
                    ],
                )
            )
            .stream()
        )
        mapping: Mapping[str, Permission] = {}
        async for documentSnapshot in stream:
            mapping[documentSnapshot.id] = Permission.fromDocumentSnapshot(
                documentSnapshot
            )
        for permissionId in permissionIds:
            permission: Optional[Permission] = mapping.get(permissionId)
            if permission is None:
                continue
            yield permission

    async def usersAvailableCount(self, tenantId: str):
        query: AsyncAggregationQuery = (
            self._collection()
            .where(filter=FieldFilter("tenantId", "==", tenantId))
            .count()
        )
        queryResultsList = await query.get()
        queryResults = next(iter(queryResultsList))
        queryResult = next(iter(queryResults))
        return int(queryResult.value)

    async def underTenant(self, tenantId: str, page: int, limit: int = PageSizes.Users):
        offset = (page - 1) * limit
        mapping: Mapping[str, Permission] = {}
        stream = (
            self._collection()
            .where(filter=FieldFilter("tenantId", "==", tenantId))
            .limit(limit)
            .offset(offset)
            .stream()
        )
        async for documentSnapshot in stream:
            permission = Permission.fromDocumentSnapshot(documentSnapshot)
            mapping[permission.get("userId")] = permission
        return mapping
