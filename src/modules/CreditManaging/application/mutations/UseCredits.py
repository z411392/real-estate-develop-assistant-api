from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient, AsyncTransaction
from src.adapters.firestore.TenantRepository import TenantRepository
from src.modules.SnapshotManaging.errors.OutOfCredits import OutOfCredits


class UseCredits:
    _logger: Logger
    _tenantRepository: TenantRepository

    def __init__(self, db: AsyncClient, transaction: AsyncTransaction):
        self._logger = createLogger(__name__)
        self._tenantRepository = TenantRepository(db=db, transaction=transaction)

    async def __call__(self, userId: str, tenantId: str, creditsToBeUsed: int = 1):
        tenant = await self._tenantRepository.get(tenantId)
        if not tenant:
            raise OutOfCredits()
        if tenant.credits < creditsToBeUsed:
            raise OutOfCredits()
        tenant.credits -= creditsToBeUsed
        await self._tenantRepository.set(tenantId, tenant)
