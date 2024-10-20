from pymupdf import Document, Pixmap
from src.utils.development import createElapsedTimeProfiler
from src.utils.storage import filePathFor, existObject, putObject, getObjectMetaData
from src.adapters.http.CloudVisionService import CloudVisionService
from os import getenv
from io import StringIO
from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient, AsyncTransaction
from src.adapters.firestore.SnapshotRepository import SnapshotRepository
from src.adapters.firestore.OwnershipRepository import OwnershipRepository
from re import search, IGNORECASE, split
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes
from src.modules.SnapshotManaging.dtos.Snapshot import Snapshot
from src.modules.IdentityAndAccessManaging.dtos.Ownership import Ownership
from src.modules.IdentityAndAccessManaging.dtos.OwnerTypes import OwnerTypes
from src.constants import Collections
from src.adapters.firestore.RegistryRepository import RegistryRepository
from src.modules.SnapshotManaging.dtos.Registry import Registry
from src.modules.SnapshotManaging.dtos.RegistryStatuses import RegistryStatuses
from typing import List


class CreateSnapshot:
    _logger: Logger
    _ocrService: CloudVisionService
    _snapshotRepository: SnapshotRepository
    _ownershipRepository: OwnershipRepository
    _registryRepository: RegistryRepository

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._logger = createLogger(__name__)
        self._ocrService = CloudVisionService(apiKey=getenv("GOOGLE_CLOUD_API_KEY"))
        self._snapshotRepository = SnapshotRepository(db=db, transaction=transaction)
        self._ownershipRepository = OwnershipRepository(db=db, transaction=transaction)
        self._registryRepository = RegistryRepository(db=db, transaction=transaction)

    async def _extractFromImage(self, buffer: bytes):
        filePath = filePathFor(buffer)
        if await existObject(filePath):
            metadata = await getObjectMetaData(filePath)
            return metadata["text"]
        else:
            text = await self._ocrService.ocr(buffer)
            await putObject(buffer, dict(text=text))
            return text

    async def _extractContentsFromImages(self, stream: bytes):
        doc = Document(stream=stream)
        for page in doc:
            pixmap: Pixmap = page.get_pixmap()
            buffer = pixmap.tobytes()
            text = await self._extractFromImage(buffer)
            yield text

    async def _extractFromPDF(self, buffer: bytes):
        text = StringIO()
        async for content in self._extractContentsFromImages(buffer):
            if content:
                text.write(content)
        return text.getvalue()

    async def _scanPDF(self, filePath: str, buffer: bytes):
        if await existObject(filePath):
            metadata = await getObjectMetaData(filePath)
            return metadata["text"]
        measureElapsedTime = createElapsedTimeProfiler()
        text = await self._extractFromPDF(buffer)
        self._logger.info(f"解析 PDF 花費了 {measureElapsedTime()} s")
        await putObject(buffer, dict(text=text))
        return text

    async def _parseSnapshot(self, filePath: str, text: str, userId: str):
        if search("建物登記第二類謄本", text, IGNORECASE):
            texts = split("本謄本列印完畢", text)
            if len(texts) == 0:
                return None
            texts = [*texts[:-1]]
            snapshotId = self._snapshotRepository.nextId(
                snapshotType=SnapshotTypes.Buildings, filePath=filePath
            )
            snapshot = Snapshot(
                type=SnapshotTypes.Buildings,
                filePath=filePath,
                userId=userId,
                id=snapshotId,
                createdAt=None,
                updatedAt=None,
            )
            registries: List[Registry] = []
            for index, text in enumerate(texts):
                registryId = RegistryRepository.nextId(
                    snapshotId=snapshotId, index=index
                )
                registry = Registry(
                    snapshotId=snapshotId,
                    index=index,
                    type=SnapshotTypes.Buildings,
                    status=RegistryStatuses.Pending,
                    text=text,
                    metadata=None,
                    id=registryId,
                    createdAt=None,
                    updatedAt=None,
                )
                registries.append(registry)
            return snapshot, registries
        return None

    async def __call__(self, userId: str, tenantId: str, filePath: str, buffer: bytes):
        """
        @todo 之後要多檢查／扣除 tenant 的 credits。
        """
        text = await self._scanPDF(filePath, buffer)
        pair = await self._parseSnapshot(filePath, text, userId)
        if pair is None:
            return None
        snapshot, registries = pair
        snapshotSnapshot = await self._snapshotRepository.get(snapshot.id)
        if not snapshotSnapshot.exists:
            await self._snapshotRepository.set(snapshot.id, snapshot)
        ownershipId = OwnershipRepository.nextId(
            ownerId=tenantId, resourceId=snapshot.id
        )
        ownershipSnapshot = await self._ownershipRepository.get(ownershipId)
        if not ownershipSnapshot.exists:
            ownership = Ownership(
                ownerId=tenantId,
                ownerType=OwnerTypes.Tenant,
                resourceId=snapshot.id,
                resourceType=str(Collections.Snapshots),
                id=ownershipId,
                createdAt=None,
                updatedAt=None,
            )
            await self._ownershipRepository.set(ownershipId, ownership)
        for registry in registries:
            registrySnapshot = await self._registryRepository.get(registry.id)
            if not registrySnapshot.exists:
                await self._registryRepository.set(registry.id, registry)
        return snapshot.id
