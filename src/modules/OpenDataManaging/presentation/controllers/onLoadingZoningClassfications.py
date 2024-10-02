from src.modules.OpenDataManaging.application.mutations.LoadZoningClassificationsForTaipeiCity import (
    LoadZoningClassificationsForTaipeiCity,
)
from firebase_admin.firestore_async import client


async def onLoadingZoningClassfications(city: str, year: int):
    db = client()
    loadZoningClassificationsForTaipeiCity = LoadZoningClassificationsForTaipeiCity(db=db)
    if city == "臺北市":
        await loadZoningClassificationsForTaipeiCity(year)
    elif city == "新北市":
        pass
