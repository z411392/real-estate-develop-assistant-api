from asyncio import create_subprocess_shell, subprocess
from src.modules.SystemMaintaining.dtos.OperationSystems import OperationSystems
from typing import Optional


class SystemService:
    async def _runShellCommand(self, command: str):
        process = await create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await process.communicate()
        error = stderr.decode('utf-8').strip()
        if error:
            raise Exception(error)
        result = stdout.decode('utf-8').strip()
        return result

    async def getOperatingSystem(self):
        uname = await self._runShellCommand("uname -s")
        if uname.find("Darwin") > -1:
            return OperationSystems.MacOS
        if uname.find("Linux") > -1:
            return OperationSystems.Linux
        if uname.find("MINGW32_NT") > -1:
            return OperationSystems.Windows32
        if uname.find("MINGW64_NT") > -1:
            return OperationSystems.Windows64
        return None

    async def getProductUUID(
            self, operatingSystem: Optional[OperationSystems]):
        if operatingSystem == OperationSystems.MacOS:
            return await self._runShellCommand("""ioreg -d2 -c IOPlatformExpertDevice | awk -F\\" '/IOPlatformUUID/{print $(NF-1)}'""")
        if operatingSystem == OperationSystems.Linux:
            return await self._runShellCommand("""cat /sys/class/dmi/id/product_uuid""")
        if operatingSystem == OperationSystems.Windows32 or operatingSystem == OperationSystems.Windows64:
            return await self._runShellCommand("""wmic csproduct get UUID""")
        return None

    async def getMacAddress(
            self, operatingSystem: Optional[OperationSystems]):
        if operatingSystem == OperationSystems.MacOS:
            return await self._runShellCommand("""ifconfig en1 | awk '/ether/{print $2}'""")
        if operatingSystem == OperationSystems.Linux:
            return await self._runShellCommand("""ip addr | grep link/ether | awk -F " " '{print $2}'|head -n 1""")
        return None
