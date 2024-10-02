from src.modules.RegistryFragmentManaging.dtos.RegistryFragmentStatuses import (
    RegistryFragmentStatuses,
)
from src.utils.events import Event
from typing import Optional


class RegistryFragmentParsed(Event):
    _registryId: str
    _fragmentId: str
    _registryFragmentStatus: RegistryFragmentStatuses
    _error: Optional[str]

    def __init__(
        self,
        registryId: str,
        fragmentId: str,
        registryFragmentStatus: RegistryFragmentStatuses,
        error: Optional[str]
    ):
        self._registryId = registryId
        self._fragmentId = fragmentId
        self._registryFragmentStatus = registryFragmentStatus
        self._error = error

    def type(self):
        return "RegistryFragmentParsed"

    def data(self):
        return dict(
            registryId=self._registryId,
            fragmentId=self._fragmentId,
            registryFragmentStatus=self._registryFragmentStatus,
            error=self._error
        )
