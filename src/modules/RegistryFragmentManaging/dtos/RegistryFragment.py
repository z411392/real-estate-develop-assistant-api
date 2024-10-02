from src.modules.RegistryFragmentManaging.dtos.RegistryFragmentParts import (
    RegistryFragmentParts,
)
from typing import Optional, TypedDict
from google.cloud.firestore import DocumentSnapshot
from datetime import datetime
from src.modules.RegistryFragmentManaging.dtos.RegistryFragmentStatuses import (
    RegistryFragmentStatuses,
)


class RegistryFragment(TypedDict):
    id: str
    part: RegistryFragmentParts
    index: int
    text: str
    tokensCount: int
    status: RegistryFragmentStatuses
    data: dict()
    createdAt: Optional[int]
    updatedAt: Optional[int]

    @staticmethod
    def fromDocumentSnapshot(documentSnapshot: DocumentSnapshot):
        createTime: datetime = documentSnapshot.create_time
        createdAt = int(createTime.timestamp() * 1000)
        updateTime: datetime = documentSnapshot.update_time
        updatedAt = int(updateTime.timestamp() * 1000)
        return RegistryFragment(
            **documentSnapshot.to_dict(),
            id=documentSnapshot.id,
            createdAt=createdAt,
            updatedAt=updatedAt
        )
