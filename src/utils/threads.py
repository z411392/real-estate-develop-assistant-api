from src.bootstrap import container
from concurrent.futures import ThreadPoolExecutor
from asyncio import wrap_future
from contextlib import asynccontextmanager


@asynccontextmanager
async def threadPoolSubmitter():
    threadPoolExecutor: ThreadPoolExecutor = await container.threadPoolExecutor()

    async def runInTheadPool(*args):
        return await wrap_future(threadPoolExecutor.submit(*args))
    yield runInTheadPool
