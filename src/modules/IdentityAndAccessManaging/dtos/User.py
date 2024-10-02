from dataclasses import dataclass


@dataclass
class User:
    id: str
    displayName: str
    photoURL: str
    createdAt: int
    updatedAt: int
