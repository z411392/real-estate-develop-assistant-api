from google.cloud.firestore import (
    AsyncClient,
    AsyncTransaction,
    DocumentSnapshot,
)
from src.constants import Collections
from src.modules.RegistryFragmentManaging.dtos.RegistryFragment import RegistryFragment
from src.modules.RegistryFragmentManaging.dtos.RegistryFragmentParts import (
    RegistryFragmentParts,
)


class RegistryFragmentRepository:
    _db: AsyncClient
    _transaction: AsyncTransaction

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._db = db
        self._transaction = transaction

    @staticmethod
    def nextId(order: int, part: RegistryFragmentParts, index: int):
        return f"{str(order).zfill(4)}_{str(part)}_{str(index).zfill(4)}"

    def _collection(self, snapshotId: str, registryId: str):
        return self._db.collection(
            str(Collections.RegistryFragments)
            .replace(":snapshotId", snapshotId)
            .replace(":registryId", registryId)
        )

    async def get(self, snapshotId: str, registryId: str, fragmentId: str):
        collection = self._collection(snapshotId, registryId)
        documentSnapshot: DocumentSnapshot = await collection.document(fragmentId).get(
            transaction=self._transaction
        )
        return (
            RegistryFragment.fromDocumentSnapshot(documentSnapshot)
            if documentSnapshot.exists
            else None
        )

    async def set(
        self,
        snapshotId: str,
        registryId: str,
        fragmentId: str,
        fragment: RegistryFragment,
    ):
        collection = self._collection(snapshotId, registryId)
        documentReference = collection.document(fragmentId)
        documentData = fragment.copy()
        if documentData.get("id"):
            del documentData["id"]
        if documentData.get("createdAt"):
            del documentData["createdAt"]
        if documentData.get("updatedAt"):
            del documentData["updatedAt"]
        self._transaction.set(documentReference, documentData, merge=True)
