from logging import Logger
from google.cloud.firestore import AsyncClient, AsyncTransaction
from src.adapters.http.OpenAIService import OpenAIService
from os import getenv
from abc import ABCMeta, abstractmethod
from src.adapters.firestore.RegistryFragmentRepository import RegistryFragmentRepository
from src.modules.RegistryFragmentManaging.dtos.RegistryFragmentStatuses import (
    RegistryFragmentStatuses,
)
from src.utils.storage import existObject, uploadFromString, downloadAsString
from src.modules.RegistryFragmentManaging.dtos.RegistryFragment import RegistryFragment
from src.adapters.firestore.EventPublisher import EventPublisher
from src.modules.SnapshotManaging.events.RegistryFragmentParsed import (
    RegistryFragmentParsed,
)
from src.constants import Collections
from typing import Optional
from src.utils.development import createLogger
from traceback import format_exc


class ParseRegistry(metaclass=ABCMeta):
    _openAIService: OpenAIService
    _registryFragmentRepository: RegistryFragmentRepository
    _eventPublisher: EventPublisher
    _logger: Logger

    def __init__(
        self,
        db: AsyncClient,
        transaction: AsyncTransaction,
    ):
        self._openAIService = OpenAIService(
            apiKey=getenv("OPENAI_API_KEY"),
        )
        self._registryFragmentRepository = RegistryFragmentRepository(
            db=db, transaction=transaction
        )
        self._eventPublisher = EventPublisher(db=db)
        self._logger = createLogger(__name__)

    def _cachePath(self, snapshotId: str, registryId: str, fragmentId: str):
        return f"json/{snapshotId}/{registryId}/{fragmentId}"

    async def _loadFromCache(self, cachePath: str):
        exists = await existObject(cachePath)
        hit = await downloadAsString(cachePath) if exists else None
        return hit

    async def _saveToCache(self, cachePath: str, data: str):
        await uploadFromString(cachePath, data)

    @abstractmethod
    async def _parseFragment(
        self, snapshotId: str, registryId: str, fragment: RegistryFragment
    ):
        return NotImplemented

    async def __call__(
        self,
        snapshotId: str,
        registryId: str,
        fragmentId: str,
    ):
        fragment = await self._registryFragmentRepository.get(
            snapshotId, registryId, fragmentId
        )
        error: Optional[Exception] = None
        try:
            self._logger.info("開始解析")
            fragment["data"] = await self._parseFragment(
                snapshotId, registryId, fragment
            )
            fragment["status"] = RegistryFragmentStatuses.Done
            self._logger.info("解析成功")
        except Exception as exception:
            self._logger.error(format_exc())
            error = exception
            fragment["status"] = RegistryFragmentStatuses.Failed
        path = str(Collections.SnapshotEvents).replace(":snapshotId", snapshotId)
        await self._eventPublisher.publish(
            path,
            RegistryFragmentParsed(
                registryId=registryId,
                fragmentId=fragmentId,
                registryFragmentStatus=fragment.get("status"),
                error=str(error),
            ),
        )
        await self._registryFragmentRepository.set(
            snapshotId, registryId, fragmentId, fragment
        )
