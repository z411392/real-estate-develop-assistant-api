from firebase_admin import db
from src.modules.SnapshotManaging.dtos.BuildingRegistry import BuildingRegistry
from typing import Optional
from src.utils.threads import ThreadPoolExecutor
from src.modules.SnapshotManaging.dtos.LandRegistry import LandRegistry


class RealtimeDatabaseDao:

    def _touchBuildingRegistry(self, registryId: str, metadata: BuildingRegistry):
        ref = db.reference(
            f"建物/{metadata.謄本核發機關}/{metadata.行政區}/{metadata.地段}/{metadata.小段}/{metadata.建號}"
        )
        record: Optional[dict] = ref.get()
        renewing = False
        if record is not None:
            updatedAt, registryId = next(iter(record.items()))
            renewing = int(updatedAt) >= metadata.列印時間
        if renewing:
            ref.set({metadata.列印時間: registryId})

    async def touchBuildingRegistry(self, registryId: str, metadata: BuildingRegistry):
        async with ThreadPoolExecutor() as execute:
            return await execute(self._touchBuildingRegistry, registryId, metadata)

    def _touchLandRegistry(self, registryId: str, metadata: LandRegistry):
        ref = db.reference(
            f"土地/{metadata.謄本核發機關}/{metadata.行政區}/{metadata.地段}/{metadata.小段}/{metadata.地號}"
        )
        record: Optional[dict] = ref.get()
        renewing = False
        if record is not None:
            updatedAt, registryId = next(iter(record.items()))
            renewing = int(updatedAt) >= metadata.列印時間
        if renewing:
            ref.set({metadata.列印時間: registryId})

    async def touchLandRegistry(self, registryId: str, metadata: LandRegistry):
        async with ThreadPoolExecutor() as execute:
            return await execute(self._touchLandRegistry, registryId, metadata)
