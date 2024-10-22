from google.cloud.firestore import AsyncClient, AsyncCollectionReference, FieldFilter
from google.cloud.firestore_v1.field_path import FieldPath
from google.cloud.firestore_v1.async_query import AsyncAggregationQuery
from src.constants import Collections
from typing import List, Mapping, Optional
from src.modules.SnapshotManaging.dtos.Registry import Registry


class RegistryDao:
    _collection: AsyncCollectionReference

    def __init__(self, db: AsyncClient):
        self._collection = db.collection(str(Collections.Registries))

    async def registriesAvailableCount(self, snapshotId: str):
        query: AsyncAggregationQuery = self._collection.where(
            filter=FieldFilter("snapshotId", "==", snapshotId)
        ).count()
        queryResultsList = await query.get()
        queryResults = next(iter(queryResultsList))
        queryResult = next(iter(queryResults))
        return int(queryResult.value)

    async def registriesAvailable(
        self,
        snapshotId: str,
    ):
        registryIds: List[str] = []
        stream = (
            self._collection.where(filter=FieldFilter("snapshotId", "==", snapshotId))
            .select(field_paths=[])
            .order_by("index")
            .select([])
            .stream()
        )
        async for documentSnapshot in stream:
            registryId = documentSnapshot.id
            registryIds.append(registryId)
        return registryIds

    async def byId(self, registryId: str):
        registry: Optional[Registry] = None
        async for found in self.inIds(registryId):
            registry = found
            break
        return registry

    async def _inIds(self, *registryIds: List[str]):
        stream = self._collection.where(
            filter=FieldFilter(
                FieldPath.document_id(),
                "in",
                [self._collection.document(registryId) for registryId in registryIds],
            )
        ).stream()

        ids: List[str] = []
        mapping: Mapping[str, Registry] = {}
        async for documentSnapshot in stream:
            ids.append(documentSnapshot.id)
            mapping[documentSnapshot.id] = Registry.fromDocumentSnapshot(documentSnapshot)
        for registryId in registryIds:
            registry: Optional[Registry] = mapping.get(registryId)
            if registry is None:
                continue
            yield registry

    async def inIds(self, *registryIds: List[str]):
        batchSize = 30
        for index in range(0, len(registryIds), batchSize):
            async for registry in self._inIds(*registryIds[index: index + batchSize]):
                yield registry
