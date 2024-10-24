from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient
from os.path import exists
from aiofile import async_open
from aiocsv import AsyncReader
from src.utils.formatters import fromArabicNumeralsToChineseNumerals
from src.constants import DocumentPaths


class LoadZoningClassificationsForTaipeiCity:
    _logger: Logger

    def __init__(self, db: AsyncClient):
        self._logger = createLogger(__name__)
        self._db = db

    async def __call__(self, year: int):
        path = f"data/zoningClassifications/臺北市/{year}.csv"  # https://data.gov.tw/dataset/145623
        if not exists(path):
            return
        batch = self._db.batch()
        batchSize = 0
        index = -1
        async with async_open(path, mode="r", encoding="utf-8") as file:
            async for row in AsyncReader(file):
                index += 1
                if index == 0:
                    continue
                [
                    _,
                    _,
                    _,
                    administrativeDistrict,
                    section,
                    subsection,
                    parentLotNumber,
                    subLotNumber,
                    zoningClassification,
                ] = list(map(str.strip, row))
                section = f"{section}段"
                if subsection.isdigit():
                    if subsection == "0":
                        subsection = "空白"
                    else:
                        subsection = f"{fromArabicNumeralsToChineseNumerals(int(subsection))}小段"
                else:
                    subsection = f"{subsection}小段"
                parentLotNumber = parentLotNumber.zfill(4)
                subLotNumber = subLotNumber.zfill(4)
                documentPath = (
                    DocumentPaths.Lands.replace(":city", "臺北市")
                    .replace(":administrativeDistrict", administrativeDistrict)
                    .replace(":section", section)
                    .replace(":subsection", subsection)
                    .replace(":parentLotNumber", parentLotNumber)
                    .replace(":subLotNumber", subLotNumber)
                    .replace(":year", year)
                )
                self._logger.info(f"正在匯入 {documentPath}")
                documentData = dict(zoningClassification=zoningClassification)
                batch.set(self._db.document(documentPath), documentData, merge=True)
                batchSize += 1
                if batchSize == 500:
                    await batch.commit()
                    batchSize = 0
                    batch = self._db.batch()
        if batchSize:
            await batch.commit()
            batchSize = 0
            batch = None
