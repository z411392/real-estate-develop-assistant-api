from re import search, IGNORECASE
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes
from src.modules.SnapshotManaging.dtos.Regexps import (
    ForBuilding,
    ForLand,
)


def determineSnapshotType(text: str):
    if search(ForBuilding, text, IGNORECASE):
        return SnapshotTypes.Building
    if search(ForLand, text, IGNORECASE):
        return SnapshotTypes.Land
    return None
