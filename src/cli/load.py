from typer import Option
from typing_extensions import Annotated
from src.modules.OpenDataManaging.dtos.DataSheetTypes import DataSheetTypes
from src.modules.OpenDataManaging.presentation.controllers.onLoadingAssessedCurrentLandValues import (
    onLoadingAssessedCurrentLandValues,
)
from src.modules.OpenDataManaging.presentation.controllers.onLoadingZoningClassfications import (
    onLoadingZoningClassfications,
)
from src.bootstrap import bootstrap


async def load(
    type: Annotated[str, Option(help="type")],
    city: Annotated[str, Option(help="city")],
    year: Annotated[int, Option(help="year")],
):
    async with bootstrap():
        if type == DataSheetTypes.AssessedCurrentLandValues:
            return await onLoadingAssessedCurrentLandValues(city, year)

        if type == DataSheetTypes.ZoningClassifications:
            return await onLoadingZoningClassfications(city, year)
