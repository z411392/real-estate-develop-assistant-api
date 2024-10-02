from firebase_admin.firestore_async import client
from src.modules.SnapshotManaging.dtos.SnapshotTypes import SnapshotTypes
from src.adapters.firestore.RegistryFragmentDao import RegistryFragmentDao
from src.modules.RegistryFragmentManaging.application.mutations.ParseBuildingRegistry import (
    ParseBuildingRegistry,
)
from src.modules.RegistryFragmentManaging.application.mutations.ParseLandRegistry import (
    ParseLandRegistry,
)
from google.cloud.firestore import async_transactional
from typing import Tuple
from asyncio import Queue, create_task, gather


async def Worker(queue: Queue[Tuple[str, str, str, SnapshotTypes]], number: int):
    while True:
        snapshotId, registryId, fragmentId, type = await queue.get()
        if type == SnapshotTypes.Building:
            db = client()

            @async_transactional
            async def runInTransaction(transaction):
                parseRegistry = ParseBuildingRegistry(
                    db=db,
                    transaction=transaction,
                )
                await parseRegistry(snapshotId, registryId, fragmentId)

            await runInTransaction(db.transaction())

        elif type == SnapshotTypes.Land:
            db = client()

            @async_transactional
            async def runInTransaction(transaction):
                parseRegistry = ParseLandRegistry(
                    db=db,
                    transaction=transaction,
                )
                await parseRegistry(snapshotId, registryId, fragmentId)

            await runInTransaction(db.transaction())
        queue.task_done()


async def onParsingRegistry(
    snapshotId: str,
    registryId: str,
    type: SnapshotTypes,
):
    db = client()
    registryFragmentDao = RegistryFragmentDao(db=db)
    fragmentIds = await registryFragmentDao.available(snapshotId, registryId)
    queue = Queue[Tuple[str, str, str, SnapshotTypes]]()
    workers = [create_task(Worker(queue, number)) for number in range(8)]
    for fragmentId in fragmentIds:
        await queue.put((snapshotId, registryId, fragmentId, type))
    await queue.join()
    for worker in workers:
        worker.cancel()
    await gather(*workers, return_exceptions=True)
