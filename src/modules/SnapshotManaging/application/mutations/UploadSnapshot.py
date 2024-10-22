from pymupdf import Document
from src.utils.development import createElapsedTimeProfiler
from src.utils.storage import filePathFor, existObject, putObject, getObjectMetaData
from src.adapters.http.OCRService import OCRService
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
from typing import List, Optional
from src.modules.SnapshotManaging.dtos.UploadingSnapshot import UploadingSnapshot
from src.modules.SnapshotManaging.errors.MustBeInPDFFormat import MustBeInPDFFormat
from base64 import b64decode


class UploadSnapshot:
    _logger: Logger
    _ocrService: OCRService
    _snapshotRepository: SnapshotRepository
    _ownershipRepository: OwnershipRepository
    _registryRepository: RegistryRepository

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._logger = createLogger(__name__)
        self._ocrService = OCRService(apiKey=getenv("OCRSPACE_API_KEY"))
        self._snapshotRepository = SnapshotRepository(db=db, transaction=transaction)
        self._ownershipRepository = OwnershipRepository(db=db, transaction=transaction)
        self._registryRepository = RegistryRepository(db=db, transaction=transaction)

    def _extractBlocks(self, buffer: bytes):
        doc = Document(stream=buffer)
        for page in doc:
            dict = page.get_text("dict")
            blocks = dict["blocks"]
            for block in blocks:
                yield block

    def _extractFromTextBlock(self, block: dict):
        for line in block["lines"]:
            for span in line["spans"]:
                text: str = span["text"]
                yield text.strip()

    async def _extractFromImageBlock(self, block: dict):
        width: int = block["width"]
        height: int = block["height"]
        ratio = width // height
        if ratio < 2:
            return None
        buffer: bytes = block["image"]
        filePath = filePathFor(buffer)
        if await existObject(filePath):
            metadata = await getObjectMetaData(filePath)
            return metadata["text"]
        else:
            text = await self._ocrService.ocr(buffer)
            await putObject(buffer, dict(text=text))
            return text

    async def _extractContents(self, buffer: bytes):
        for block in self._extractBlocks(buffer):
            if block["type"] == 0:
                for content in self._extractFromTextBlock(block):
                    if content:
                        yield True, f"\n{content}"
            if block["type"] == 1:
                content = await self._extractFromImageBlock(block)
                if content:
                    yield False, f"\n{content}"

    async def _extractFromPDF(self, buffer: bytes):
        text = StringIO()
        textsCount = 0
        async for isText, content in self._extractContents(buffer):
            text.write(content)
            if isText:
                textsCount += 1
        return text.getvalue() if textsCount > 0 else ""

    async def _scanPDF(self, filePath: str, buffer: bytes):
        if await existObject(filePath):
            metadata = await getObjectMetaData(filePath)
            return metadata["text"]
        measureElapsedTime = createElapsedTimeProfiler()
        text = await self._extractFromPDF(buffer)
        self._logger.info(f"解析 PDF 花費了 {measureElapsedTime()} s")
        await putObject(buffer, dict(text=text))
        return text

    async def _createRegistry(self, name: str, filePath: str, text: str, userId: str):
        snapshotType: Optional[SnapshotTypes] = None
        if search(r"建物登記第(?:一|二|三)類謄本", text, IGNORECASE):
            snapshotType = SnapshotTypes.Building
        if search(r"土地登記第(?:一|二|三)類謄本", text, IGNORECASE):
            snapshotType = SnapshotTypes.Land
        if snapshotType is None:
            return None
        texts = split(".*本謄本列印完畢.*", text)
        texts = [texts[-1] + texts[0], *texts[1:-1]]
        snapshotId = self._snapshotRepository.nextId(
            snapshotType=snapshotType, filePath=filePath
        )
        snapshot = Snapshot(
            name=name,
            type=snapshotType,
            filePath=filePath,
            userId=userId,
            id=snapshotId,
            createdAt=None,
            updatedAt=None,
        )
        registries: List[Registry] = []
        for index, text in enumerate(texts):
            registryId = RegistryRepository.nextId(snapshotId=snapshotId, index=index)
            registry = Registry(
                snapshotId=snapshotId,
                index=index,
                type=snapshotType,
                status=RegistryStatuses.Pending,
                text=text,
                metadata=None,
                id=registryId,
                createdAt=None,
                updatedAt=None,
            )
            registries.append(registry)
        return snapshot, registries

    async def __call__(self, userId: str, tenantId: str, mutation: UploadingSnapshot):
        buffer = b64decode(mutation.content)
        filePath = filePathFor(buffer)
        if not filePath.startswith("pdf"):
            raise MustBeInPDFFormat()
        text = await self._scanPDF(filePath, buffer)
        pair = await self._createRegistry(mutation.name, filePath, text, userId)
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
