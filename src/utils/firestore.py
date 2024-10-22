from google.cloud.firestore import AsyncClient, AsyncTransaction, async_transactional
from contextlib import AbstractAsyncContextManager
from asyncio import Future, get_event_loop


class Transaction(AbstractAsyncContextManager):
    _db: AsyncClient
    _future: Future

    def __init__(self, db: AsyncClient):
        self._db = db
        self._future = get_event_loop().create_future()

    async def __aenter__(self):
        future = get_event_loop().create_future()

        @async_transactional
        async def runInTransaction(transaction: AsyncTransaction):
            future.set_result(transaction)
            await self._future

        get_event_loop().create_task(runInTransaction(self._db.transaction()))
        transaction: AsyncTransaction = await future
        return transaction

    async def __aexit__(self, exceptionType, exception, traceback):
        self._future.set_result(None)
        if exceptionType:
            return False
