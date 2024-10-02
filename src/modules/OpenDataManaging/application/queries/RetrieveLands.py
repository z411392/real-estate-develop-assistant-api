from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient
from src.constants import DocumentPaths
from datetime import datetime
from src.modules.OpenDataManaging.dtos.Land import Land
from typing import Optional, List, TypedDict


class LandDescriptor(TypedDict):
    city: str
    administrativeDistrict: str
    section: str
    subsection: str
    parentLotNumber: str
    subLotNumber: str


class RetrievingLands(TypedDict):
    landDescriptors: List[LandDescriptor]


class RetrieveLands:
    _logger: Logger
    _db: AsyncClient

    def __init__(self, db: AsyncClient):
        self._logger = createLogger(__name__)
        self._db = db

    async def __call__(self, userId: str, tenantId: str, query: RetrievingLands):
        now = datetime.now()
        for landDescriptor in query.get("landDescriptors"):
            documentPath = (
                DocumentPaths.Lands.replace(":city", landDescriptor.get("city"))
                .replace(
                    ":administrativeDistrict",
                    landDescriptor.get("administrativeDistrict"),
                )
                .replace(":section", landDescriptor.get("section"))
                .replace(":subsection", landDescriptor.get("subsection"))
                .replace(":parentLotNumber", landDescriptor.get("parentLotNumber"))
                .replace(":subLotNumber", landDescriptor.get("subLotNumber"))
                .replace(":year", str(now.year))
            )
            documentSnapshot = await self._db.document(documentPath).get()

            zoningClassification: Optional[str] = None
            assessedCurrentValue: Optional[int] = None
            if documentSnapshot.exists:
                data = documentSnapshot.to_dict()
                zoningClassification = (
                    str(data.get("zoningClassification"))
                    if data.get("zoningClassification")
                    else None
                )
                assessedCurrentValue = (
                    int(data.get("assessedCurrentValue"))
                    if data.get("assessedCurrentValue")
                    else None
                )
            land = Land(
                **landDescriptor,
                zoningClassification=zoningClassification,
                assessedCurrentValue=assessedCurrentValue,
                year=str(now.year),
            )
            yield land
