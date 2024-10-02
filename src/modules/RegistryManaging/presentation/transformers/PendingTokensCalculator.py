from src.modules.RegistryFragmentManaging.dtos.RegistryFragment import RegistryFragment
from src.modules.RegistryFragmentManaging.dtos.RegistryFragmentStatuses import (
    RegistryFragmentStatuses,
)


class PendingTokensCalculator:
    _tokensCount: int

    def __init__(self):
        self._tokensCount = 0

    def accumulated(self):
        return self._tokensCount

    def __call__(self, fragment: RegistryFragment):
        if fragment.get("status") != RegistryFragmentStatuses.Pending:
            return
        self._tokensCount += fragment.get("tokensCount")
