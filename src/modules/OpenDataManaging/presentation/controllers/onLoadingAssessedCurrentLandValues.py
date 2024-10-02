from src.modules.OpenDataManaging.application.mutations.LoadAssessedCurrentLandValuesForTaipeiCity import (
    LoadAssessedCurrentLandValuesForTaipeiCity,
)
from src.modules.OpenDataManaging.application.mutations.LoadAssessedCurrentLandValuesForNewTaipeiCity import LoadAssessedCurrentLandValuesForNewTaipeiCity
from firebase_admin.firestore_async import client


async def onLoadingAssessedCurrentLandValues(city: str, year: int):
    db = client()
    if city == "臺北市":
        loadValueAnnouncedForTaipeiCity = LoadAssessedCurrentLandValuesForTaipeiCity(db=db)
        await loadValueAnnouncedForTaipeiCity(year)
    elif city == "新北市":
        loadAssessedCurrentLandValuesForNewTaipeiCity = LoadAssessedCurrentLandValuesForNewTaipeiCity(db=db)
        await loadAssessedCurrentLandValuesForNewTaipeiCity(year)
