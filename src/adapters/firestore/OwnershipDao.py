from google.cloud.firestore import AsyncClient, FieldFilter
from google.cloud.firestore_v1.field_path import FieldPath
from google.cloud.firestore_v1.async_query import AsyncAggregationQuery
from src.constants import Collections
from src.modules.IdentityAndAccessManaging.dtos.Ownership import Ownership
from src.modules.IdentityAndAccessManaging.dtos.OwnerTypes import OwnerTypes
from src.constants import PageSizes
from typing import List, Mapping, Optional
from operator import itemgetter


class OwnershipDao:
    _db: AsyncClient

    def __init__(self, db: AsyncClient):
        self._db = db

    def _collection(self):
        return self._db.collection(str(Collections.Ownerships))

    async def snapshotsAvailableCount(self, tenantId: str):
        query: AsyncAggregationQuery = (
            self._collection()
            .where(filter=FieldFilter("ownerType", "==", str(OwnerTypes.Tenant)))
            .where(filter=FieldFilter("ownerId", "==", tenantId))
            .where(filter=FieldFilter("resourceType", "==", str(Collections.Snapshots)))
            .count()
        )
        queryResultsList = await query.get()
        queryResults = next(iter(queryResultsList))
        queryResult = next(iter(queryResults))
        return int(queryResult.value)

    async def snapshotsAvailable(
        self, tenantId: str, page: int, limit: int = PageSizes.Snapshots
    ):
        offset = (page - 1) * limit
        snapshotIds: List[str] = []
        stream = (
            self._collection()
            .where(filter=FieldFilter("ownerType", "==", str(OwnerTypes.Tenant)))
            .where(filter=FieldFilter("ownerId", "==", tenantId))
            .where(filter=FieldFilter("resourceType", "==", str(Collections.Snapshots)))
            .limit(limit)
            .offset(offset)
            .select(["resourceId"])
            .stream()
        )
        async for documentSnapshot in stream:
            snapshotId = itemgetter("resourceId")(documentSnapshot.to_dict())
            snapshotIds.append(snapshotId)
        return snapshotIds

    async def byId(self, ownershipId: str):
        ownership: Optional[Ownership] = None
        async for found in self.inIds(ownershipId):
            ownership = found
            break
        return ownership

    async def inIds(self, *ownershipIds: List[str]):
        stream = (
            self._collection()
            .where(
                filter=FieldFilter(
                    FieldPath.document_id(),
                    "in",
                    [
                        self._collection().document(ownershipId)
                        for ownershipId in ownershipIds
                    ],
                )
            )
            .stream()
        )
        mapping: Mapping[str, Ownership] = {}
        async for documentSnapshot in stream:
            mapping[documentSnapshot.id] = Ownership.fromDocumentSnapshot(
                documentSnapshot
            )
        for ownershipId in ownershipIds:
            ownership: Optional[Ownership] = mapping.get(ownershipId)
            if ownership is None:
                continue
            yield ownership
