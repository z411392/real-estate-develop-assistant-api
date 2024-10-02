from google.cloud.firestore import AsyncClient, FieldFilter
from google.cloud.firestore_v1.field_path import FieldPath
from google.cloud.firestore_v1.async_query import AsyncAggregationQuery
from src.constants import Collections
from typing import List, Mapping, Optional
from src.modules.RegistryManaging.dtos.Registry import Registry


class RegistryDao:
    _db: AsyncClient

    def __init__(self, db: AsyncClient):
        self._db = db

    def _collection(self, snapshotId: str):
        return self._db.collection(
            str(Collections.Registries).replace(":snapshotId", snapshotId)
        )

    async def registriesAvailableCount(self, snapshotId: str):
        collection = self._collection(snapshotId)
        query: AsyncAggregationQuery = collection.count()
        queryResultsList = await query.get()
        queryResults = next(iter(queryResultsList))
        queryResult = next(iter(queryResults))
        return int(queryResult.value)

    async def registriesAvailable(
        self,
        snapshotId: str,
    ):
        registryIds: List[str] = []
        collection = self._collection(snapshotId)
        stream = collection.select(field_paths=[]).order_by("index").select([]).stream()
        async for documentSnapshot in stream:
            registryId = documentSnapshot.id
            registryIds.append(registryId)
        return registryIds

    async def byId(self, snapshotId: str, registryId: str):
        registry: Optional[Registry] = None
        async for found in self.inIds(snapshotId, registryId):
            registry = found
            break
        return registry

    async def _inIds(self, snapshotId: str, *registryIds: List[str]):
        collection = self._collection(snapshotId)
        identifiers = [collection.document(registryId) for registryId in registryIds]
        stream = collection.where(
            filter=FieldFilter(
                FieldPath.document_id(),
                "in",
                identifiers,
            )
        ).stream()
        mapping: Mapping[str, Registry] = {}
        async for documentSnapshot in stream:
            mapping[documentSnapshot.id] = Registry.fromDocumentSnapshot(
                documentSnapshot
            )
        for registryId in registryIds:
            registry: Optional[Registry] = mapping.get(registryId)
            if registry is None:
                continue
            yield registry

    async def inIds(self, snapshotId: str, *registryIds: List[str]):
        batchSize = 30
        for index in range(0, len(registryIds), batchSize):
            async for registry in self._inIds(
                snapshotId, *registryIds[index: index + batchSize]
            ):
                yield registry
