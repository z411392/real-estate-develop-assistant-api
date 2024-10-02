from logging import Logger
from src.utils.development import createLogger
from google.cloud.firestore import AsyncClient, AsyncTransaction
from src.adapters.firestore.RegistryRepository import RegistryRepository
from src.modules.RegistryManaging.errors.RegistryNotFound import RegistryNotFound
from src.utils.calculators import countCreditsToBeUsed
from src.modules.RegistryManaging.errors.OutOfCredits import OutOfCredits
from src.adapters.firestore.TenantRepository import TenantRepository
from src.modules.TenantManaging.errors.TenantNotFound import TenantNotFound
from src.adapters.firestore.RegistryFragmentDao import RegistryFragmentDao
from src.adapters.firestore.RegistryFragmentRepository import RegistryFragmentRepository
from typing import List
from asyncio import gather
from src.modules.RegistryFragmentManaging.dtos.RegistryFragment import (
    RegistryFragment,
)
from src.modules.RegistryFragmentManaging.dtos.RegistryFragmentStatuses import (
    RegistryFragmentStatuses,
)


class StartParsingRegistry:
    _logger: Logger
    _registryRepository: RegistryRepository
    _tenantRepository: TenantRepository
    _registryFragmentDao: RegistryFragmentDao
    _registryFragmentRepository: RegistryFragmentRepository

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._logger = createLogger(__name__)
        self._registryRepository = RegistryRepository(db=db, transaction=transaction)
        self._tenantRepository = TenantRepository(db=db, transaction=transaction)
        self._registryFragmentDao = RegistryFragmentDao(db=db)
        self._registryFragmentRepository = RegistryFragmentRepository(
            db=db, transaction=transaction
        )

    async def __call__(
        self,
        userId: str,
        tenantId: str,
        snapshotId: str,
        registryId: str,
    ):
        tenant = await self._tenantRepository.get(tenantId)
        if tenant is None:
            raise TenantNotFound(tenantId=tenantId)
        registry = await self._registryRepository.get(snapshotId, registryId)
        if registry is None:
            raise RegistryNotFound(registryId=registryId)
        tokensCount = 0
        fragments: List[RegistryFragment] = []
        async for fragment in self._registryFragmentDao.all(snapshotId, registryId):
            if fragment.get("status") == RegistryFragmentStatuses.Pending:
                tokensCount += fragment.get("tokensCount")
            fragment["status"] = RegistryFragmentStatuses.Doing
            fragments.append(fragment)
        toBeDedcuted = countCreditsToBeUsed(tokensCount)
        if tenant.get("credits") < toBeDedcuted:
            raise OutOfCredits(
                remaining=tenant.get("credits"), toBeDecucted=toBeDedcuted
            )

        await gather(
            *[
                self._registryFragmentRepository.set(
                    snapshotId,
                    registryId,
                    fragment.get("id"),
                    fragment,
                )
                for fragment in fragments
            ]
        )
        await self._registryRepository.set(snapshotId, registryId, registry)
        tenant["credits"] -= toBeDedcuted
        await self._tenantRepository.set(tenantId, tenant)
        return toBeDedcuted
