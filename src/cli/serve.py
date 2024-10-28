from typing_extensions import Annotated
from typer import Option
from os import getenv
from asyncio import get_event_loop
from src.http import createApp
from uvicorn import Config, Server


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
