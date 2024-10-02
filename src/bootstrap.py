
from firebase_admin import initialize_app, credentials
from os import getenv
from re import sub
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Resource
from starlette.applications import Starlette
from contextlib import asynccontextmanager
from typing import Optional
from concurrent.futures import ThreadPoolExecutor
from psutil import cpu_count


async def initThreadPool(max_workers: int = cpu_count(logical=True)):
    threadPoolExecutor = ThreadPoolExecutor(max_workers=max_workers)
    yield threadPoolExecutor
    threadPoolExecutor.shutdown()


async def initFirebaseApp():
    credential = credentials.Certificate({
        "type": "service_account",
        "client_email": getenv("CLIENT_EMAIL"),
        "private_key": sub(r'\\n', "\n", getenv("PRIVATE_KEY")),
        "token_uri": "https://oauth2.googleapis.com/token"
    })
    options = {
        "projectId": getenv("APP"),
        "databaseURL": getenv("DATABASE_URL"),
        "storageBucket": getenv("STORAGE_BUCKET"),
    }
    app = initialize_app(credential=credential, options=options)
    yield app


class Container(DeclarativeContainer):
    config = Configuration()
    threadPoolExecutor = Resource(initThreadPool)
    firebaseApp = Resource(initFirebaseApp)


container = Container()


@asynccontextmanager
async def bootstrap(app: Optional[Starlette] = None):
    awaitable = container.init_resources()
    if awaitable is not None:
        await awaitable
    yield {} if app else None
    awaitable = container.shutdown_resources()
    if awaitable is not None:
        await awaitable
