from src.modules.OpenDataManaging.dtos.RetrievingLands import RetrievingLands
from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient
from src.constants import DocumentPaths
from datetime import datetime
from src.modules.OpenDataManaging.dtos.Land import Land
from dataclasses import asdict
from typing import Optional


class RetrieveLands:
    _logger: Logger
    _db: AsyncClient

    def __init__(self, db: AsyncClient):
        self._logger = createLogger(__name__)
        self._db = db

    async def __call__(self, userId: str, tenantId: str, query: RetrievingLands):
        now = datetime.now()
        for landDescriptor in query.landDescriptors:
            documentPath = (
                DocumentPaths.Lands.replace(":city", landDescriptor.city)
                .replace(
                    ":administrativeDistrict", landDescriptor.administrativeDistrict
                )
                .replace(":section", landDescriptor.section)
                .replace(":subsection", landDescriptor.subsection)
                .replace(":parentLotNumber", landDescriptor.parentLotNumber)
                .replace(":subLotNumber", landDescriptor.subLotNumber)
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
                **asdict(landDescriptor),
                zoningClassification=zoningClassification,
                assessedCurrentValue=assessedCurrentValue,
                year=str(now.year),
            )
            yield land
