from src.modules.RegistryFragmentManaging.dtos.RegistryFragment import RegistryFragment
from src.modules.RegistryFragmentManaging.dtos.RegistryFragmentStatuses import (
    RegistryFragmentStatuses,
)
from src.modules.RegistryManaging.dtos.RegistryStatuses import RegistryStatuses


class RegistryStatusCalculator:
    _allDone: bool
    _allPending: bool
    _someDoing: bool
    _someFailed: bool

    def __init__(self):
        self._allDone = True
        self._allPending = True
        self._someDoing = False
        self._someFailed = False

    def accumulated(self):
        if self._allDone:
            return RegistryStatuses.Done
        if self._allPending:
            return RegistryStatuses.Pending
        if self._someDoing:
            return RegistryStatuses.Doing
        if self._someFailed:
            return RegistryStatuses.Failed
        return RegistryStatuses.Doing

    def __call__(self, fragment: RegistryFragment):
        if fragment.get("status") != RegistryFragmentStatuses.Done:
            self._allDone = False
        if fragment.get("status") != RegistryFragmentStatuses.Pending:
            self._allPending = False
        if fragment.get("status") == RegistryFragmentStatuses.Failed:
            self._someFailed = True
        if fragment.get("status") == RegistryFragmentStatuses.Doing:
            self._someDoing = True
