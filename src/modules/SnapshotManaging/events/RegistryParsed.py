from src.modules.RegistryManaging.dtos.RegistryStatuses import (
    RegistryStatuses,
)
from src.utils.events import Event


class RegistryParsed(Event):
    _registryId: str
    _registryStatus: RegistryStatuses

    def __init__(
        self,
        registryId: str,
        registryStatus: RegistryStatuses,
    ):
        self._registryId = registryId
        self._registryStatus = registryStatus

    def type(self):
        return "RegistryParsed"

    def data(self):
        return dict(
            registryId=self._registryId,
            registryStatus=str(self._registryStatus),
        )
