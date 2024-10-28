from src.utils.development import createLogger
from logging import Logger
from src.adapters.system.SystemService import SystemService
from os import getenv
from src.constants import Version
from typing import Optional


class RetrieveSystemInfo:
    _logger: Logger
    _systemService: SystemService

    def __init__(self):
        self._logger = createLogger(__name__)
        self._systemService = SystemService()

    async def __call__(self, exp: Optional[int]):
        systemInfo = dict(version=Version)
        os = await self._systemService.getOperatingSystem()
        if os is not None:
            systemInfo.update(os=os)
        uuid = getenv("PROJECT_UUID")
        if uuid is None:
            uuid = await self._systemService.getProductUUID(os)
        systemInfo.update(uuid=uuid)
        mac = await self._systemService.getMacAddress(os)
        if mac is not None:
            systemInfo.update(mac=mac)
        if exp is not None:
            systemInfo.update(exp=exp)
        return systemInfo
