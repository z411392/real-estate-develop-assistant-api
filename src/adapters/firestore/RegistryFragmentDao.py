from google.cloud.firestore import AsyncClient
from src.constants import Collections
from src.modules.RegistryFragmentManaging.dtos.RegistryFragment import RegistryFragment
from typing import List


class RegistryFragmentDao:
    _db: AsyncClient

    def __init__(self, db: AsyncClient):
        self._db = db

    def _collection(self, snapshotId: str, registryId: str):
        return self._db.collection(
            str(Collections.RegistryFragments)
            .replace(":snapshotId", snapshotId)
            .replace(":registryId", registryId)
        )

    async def available(self, snapshotId: str, registryId: str):
        collection = self._collection(snapshotId, registryId)
        stream = collection.select(field_paths=[]).stream()
        fragmentIds: List[str] = []
        async for documentSnapshot in stream:
            fragmentIds.append(documentSnapshot.id)
        return fragmentIds

    async def all(self, snapshotId: str, registryId: str):
        collection = self._collection(snapshotId, registryId)
        stream = collection.stream()
        async for documentSnapshot in stream:
            yield RegistryFragment.fromDocumentSnapshot(documentSnapshot)
