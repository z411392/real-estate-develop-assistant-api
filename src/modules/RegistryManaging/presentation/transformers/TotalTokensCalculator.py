from src.modules.RegistryFragmentManaging.dtos.RegistryFragment import RegistryFragment


class TotalTokensCalculator:
    _tokensCount: int

    def __init__(self):
        self._tokensCount = 0

    def accumulated(self):
        return self._tokensCount

    def __call__(self, fragment: RegistryFragment):
        self._tokensCount += fragment.get("tokensCount")
