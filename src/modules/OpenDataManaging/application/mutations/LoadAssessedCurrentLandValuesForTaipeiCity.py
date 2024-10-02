from src.utils.development import createLogger
from logging import Logger
from google.cloud.firestore import AsyncClient
from os.path import exists
from aiofile import async_open
from aiocsv import AsyncReader
from re import match
from src.constants import DocumentPaths


class LoadAssessedCurrentLandValuesForTaipeiCity:
    _logger: Logger

    def __init__(self, db: AsyncClient):
        self._logger = createLogger(__name__)
        self._db = db

    async def __call__(self, year: int):
        path = f"data/assessedCurrentValues/臺北市/{year}.csv"  # https://data.gov.tw/dataset/122058
        if not exists(path):
            return
        batch = self._db.batch()
        batchSize = 0
        index = -1
        async with async_open(path, mode="r", encoding="big5") as file:
            async for row in AsyncReader(file):
                index += 1
                if index == 0:
                    continue
                [
                    _,
                    administrativeDistrict,
                    sectionAndSubsection,
                    parentAndSubLotNumber,
                    assessedCurrentValue,
                    _,
                ] = list(map(str.strip, row))
                section, subsection = match(
                    r"(.*?段)(.*?段)?", sectionAndSubsection
                ).groups()
                if subsection is None:
                    subsection = "空白"
                parentLotNumber = parentAndSubLotNumber[0:4]
                subLotNumber = parentAndSubLotNumber[4:]
                documentPath = (
                    DocumentPaths.Lands.replace(":city", "臺北市")
                    .replace(":administrativeDistrict", administrativeDistrict)
                    .replace(":section", section)
                    .replace(":subsection", subsection)
                    .replace(":parentLotNumber", parentLotNumber)
                    .replace(":subLotNumber", subLotNumber)
                    .replace(":year", str(year))
                )
                self._logger.info(f"正在匯入 {documentPath}")
                documentData = dict(assessedCurrentValue=int(assessedCurrentValue))
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
