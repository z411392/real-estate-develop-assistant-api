from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient, AsyncTransaction
from src.adapters.firestore.SnapshotRepository import SnapshotRepository
from src.adapters.firestore.OwnershipRepository import OwnershipRepository
from re import split
from src.modules.SnapshotManaging.dtos.Snapshot import Snapshot
from src.modules.IdentityAndAccessManaging.dtos.Ownership import Ownership
from src.modules.IdentityAndAccessManaging.dtos.OwnerTypes import OwnerTypes
from src.constants import Collections
from src.adapters.firestore.RegistryRepository import RegistryRepository
from src.modules.RegistryManaging.dtos.Registry import Registry
from src.modules.RegistryManaging.dtos.RegistryStatuses import RegistryStatuses
from typing import List, Coroutine, TypedDict
from asyncio import gather
from src.modules.SnapshotManaging.domain.services.determineSnapshotType import (
    determineSnapshotType,
)
from src.modules.RegistryManaging.domain.services.RegistryFragmentsCreator import (
    RegistryFragmentsCreator,
)
from src.modules.SnapshotManaging.domain.services.removeNotices import (
    removeNotices,
)
from src.adapters.firestore.RegistryFragmentRepository import RegistryFragmentRepository


class UploadingSnapshot(TypedDict):
    name: str
    content: str


class UploadSnapshot:
    _logger: Logger
    _snapshotRepository: SnapshotRepository
    _ownershipRepository: OwnershipRepository
    _registryRepository: RegistryRepository
    _registryFragmentRepository: RegistryFragmentRepository

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._logger = createLogger(__name__)
        self._snapshotRepository = SnapshotRepository(db=db, transaction=transaction)
        self._ownershipRepository = OwnershipRepository(db=db, transaction=transaction)
        self._registryRepository = RegistryRepository(db=db, transaction=transaction)
        self._registryFragmentRepository = RegistryFragmentRepository(
            db=db, transaction=transaction
        )

    async def _snapshotOf(self, name: str, filePath: str, text: str, userId: str):
        snapshotType = determineSnapshotType(text)
        if snapshotType is None:
            return None
        snapshotId = SnapshotRepository.nextId(
            snapshotType=snapshotType, filePath=filePath
        )
        snapshot = Snapshot(
            name=name,
            type=snapshotType,
            filePath=filePath,
            userId=userId,
            id=snapshotId,
        )
        return snapshot

    async def _registryOf(self, snapshot: Snapshot, index: int):
        registryId = RegistryRepository.nextId(
            snapshotId=snapshot.get("id"), index=index
        )
        registry = Registry(
            snapshotId=snapshot.get("id"),
            index=index,
            type=snapshot.get("type"),
            status=RegistryStatuses.Pending,
            metadata=None,
            id=registryId,
        )
        return registry

    async def _registriesOf(self, snapshot: Snapshot, fullText: str):
        segments = split(".*本謄本列印完畢.*", fullText)[:-1]
        createRegistryFragments = RegistryFragmentsCreator(snapshot.get("type"))
        for index, segment in enumerate(segments):
            text = removeNotices(snapshot.get("type"), segment)
            registry = await self._registryOf(snapshot, index)
            fragments = createRegistryFragments(text)
            yield registry, fragments

    async def __call__(
        self, userId: str, tenantId: str, name: str, fullText: str, filePath: str
    ):
        snapshot = await self._snapshotOf(name, filePath, fullText, userId)
        if snapshot is None:
            return None
        snapshotExists = await self._snapshotRepository.get(snapshot.get("id"))
        operations: List[Coroutine] = []
        if snapshotExists:
            snapshotExists["name"] = snapshot.get("name")
            snapshot = snapshotExists
        operations.append(self._snapshotRepository.set(snapshot.get("id"), snapshot))
        ownershipId = OwnershipRepository.nextId(
            ownerId=tenantId, resourceId=snapshot.get("id")
        )
        ownershipExists = await self._ownershipRepository.get(ownershipId)
        if not ownershipExists:
            ownership = Ownership(
                ownerId=tenantId,
                ownerType=OwnerTypes.Tenant,
                resourceId=snapshot.get("id"),
                resourceType=str(Collections.Snapshots),
                id=ownershipId,
            )
            operations.append(self._ownershipRepository.set(ownershipId, ownership))
        registries = self._registriesOf(snapshot, fullText)
        async for registry, fragments in registries:
            registryExists = await self._registryRepository.get(
                snapshot.get("id"), registry.get("id")
            )
            if not registryExists:
                operations.append(
                    self._registryRepository.set(
                        snapshot.get("id"), registry.get("id"), registry
                    )
                )
            for fragment in fragments:
                fragmentExists = await self._registryFragmentRepository.get(
                    snapshot.get("id"), registry.get("id"), fragment.get("id")
                )
                if not fragmentExists:
                    operations.append(
                        self._registryFragmentRepository.set(
                            snapshot.get("id"),
                            registry.get("id"),
                            fragment.get("id"),
                            fragment,
                        )
                    )
        await gather(*operations)
        return snapshot.get("id")
