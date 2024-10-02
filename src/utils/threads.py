from src.bootstrap import container
from concurrent.futures import ThreadPoolExecutor as _ThreadPoolExecutor
from asyncio import wrap_future
from contextlib import asynccontextmanager


@asynccontextmanager
async def ThreadPoolExecutor():
    threadPoolExecutor: _ThreadPoolExecutor = await container.threadPoolExecutor()

    async def submit(*args):
        return await wrap_future(threadPoolExecutor.submit(*args))

    yield submit
