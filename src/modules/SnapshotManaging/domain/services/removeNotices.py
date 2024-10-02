from re import split, search
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes
from src.modules.SnapshotManaging.dtos.Regexps import (
    ForBuilding,
    ForLand,
)
from typing import Optional


def removeNotices(type: SnapshotTypes, text: str):
    pattern: Optional[str] = None
    if type == SnapshotTypes.Building:
        pattern = ForBuilding
    if type == SnapshotTypes.Land:
        pattern = ForLand
    if pattern is None:
        return text
    found = search(pattern, text)
    if found is None:
        return text
    [_, content] = split(pattern, text, maxsplit=1)
    return f"{found.group(0)}\n\n{content}"
