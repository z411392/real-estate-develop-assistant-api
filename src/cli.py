from async_typer import AsyncTyper
from typer import Option
from typing_extensions import Annotated
from os import getenv
from asyncio import get_event_loop
from src.http import createApp
from uvicorn import Config, Server
from src.modules.OpenDataManaging.dtos.DataSheetTypes import DataSheetTypes
from src.modules.OpenDataManaging.presentation.controllers.onLoadingAssessedCurrentLandValues import (
    onLoadingAssessedCurrentLandValues,
)
from src.modules.OpenDataManaging.presentation.controllers.onLoadingZoningClassfications import (
    onLoadingZoningClassfications,
)
from src.bootstrap import bootstrap

app = AsyncTyper()


@app.async_command()
async def serve(
    host: Annotated[str, Option(help="host")] = "0.0.0.0",
    port: Annotated[int, Option(help="port")] = int(getenv("PORT")),
):
    loop = get_event_loop()
    app = createApp()
    config = Config(
        app=app,
        host=host,
        port=port,
        loop=loop,
        server_header=False,
        date_header=False,
    )
    server = Server(config=config)
    return await server.serve()


@app.async_command()
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
