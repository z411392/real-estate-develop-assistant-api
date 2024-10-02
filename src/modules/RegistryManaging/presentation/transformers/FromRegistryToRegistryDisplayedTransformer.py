from src.modules.RegistryManaging.dtos.Registry import Registry
from typing import AsyncIterable
from src.modules.RegistryFragmentManaging.dtos.RegistryFragment import (
    RegistryFragment,
)
from src.modules.RegistryManaging.presentation.transformers.TextComposer import (
    TextComposer,
)
from src.modules.RegistryManaging.presentation.transformers.TotalTokensCalculator import (
    TotalTokensCalculator,
)
from src.modules.RegistryManaging.presentation.transformers.ProcessedTokensCalculator import (
    ProcessedTokensCalculator,
)
from src.modules.RegistryManaging.presentation.transformers.MetadataBuilder import (
    MetadataBuilder,
)
from src.modules.RegistryManaging.presentation.transformers.RegistryStatusCalculator import (
    RegistryStatusCalculator,
)
from src.modules.RegistryManaging.presentation.transformers.PendingTokensCalculator import (
    PendingTokensCalculator,
)
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes


class FromRegistryToRegistryDisplayedTransformer:
    _textComposer: TextComposer
    _totalTokensCalculator: TotalTokensCalculator
    _processedTokensCalculator: ProcessedTokensCalculator
    _metadataBuilder: MetadataBuilder
    _registryStatusCalculator: RegistryStatusCalculator
    _pendingTokensCalculator: PendingTokensCalculator

    def __init__(self, type: SnapshotTypes):
        self._textComposer = TextComposer(type)
        self._totalTokensCalculator = TotalTokensCalculator()
        self._processedTokensCalculator = ProcessedTokensCalculator()
        self._metadataBuilder = MetadataBuilder(type)
        self._registryStatusCalculator = RegistryStatusCalculator()
        self._pendingTokensCalculator = PendingTokensCalculator()

    async def __call__(
        self, registry: Registry, fragments: AsyncIterable[RegistryFragment]
    ):
        async for fragment in fragments:
            self._textComposer(fragment)
            self._totalTokensCalculator(fragment)
            self._processedTokensCalculator(fragment)
            self._metadataBuilder(fragment)
            self._registryStatusCalculator(fragment)
            self._pendingTokensCalculator(fragment)
        text = self._textComposer.accumulated()
        totalTokens = self._totalTokensCalculator.accumulated()
        processedTokens = self._processedTokensCalculator.accumulated()
        metadata = self._metadataBuilder.accumulated()
        registryStatus = self._registryStatusCalculator.accumulated()
        pendingTokens = self._pendingTokensCalculator.accumulated()
        transformed = dict(
            id=registry.get("id"),
            snapshotId=registry.get("snapshotId"),
            type=registry.get("type"),
            status=registryStatus,
            text=text,
            metadata=metadata,
            pending=pendingTokens,
            total=totalTokens,
            processed=processedTokens,
            index=registry.get("index"),
            createdAt=registry.get("createdAt"),
            updatedAt=registry.get("updatedAt"),
        )
        return transformed
