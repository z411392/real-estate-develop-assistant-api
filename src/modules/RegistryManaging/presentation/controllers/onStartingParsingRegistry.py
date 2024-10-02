from starlette.requests import Request
from src.utils.sessions import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    ensureUserHasPermission,
    ensureSnapshotIsSpecified,
)
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.RegistryManaging.application.mutations.StartParsingRegistry import (
    StartParsingRegistry,
)
from starlette.background import BackgroundTask
from src.modules.RegistryFragmentManaging.presentation.controllers.onParsingRegistry import (
    onParsingRegistry,
)
from google.cloud.firestore import async_transactional


async def onStartingParsingRegistry(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    snapshot = ensureSnapshotIsSpecified(request)
    registryId = request.path_params.get("registryId")
    db = client()
    payload = dict()

    @async_transactional
    async def runInTransaction(transaction):
        startParsingRegistry = StartParsingRegistry(db=db, transaction=transaction)
        toBeDedcuted = await startParsingRegistry(
            credentials.get("uid"),
            tenant.get("id"),
            snapshot.get("id"),
            registryId,
        )
        payload.update(toBeDedcuted=toBeDedcuted)

    await runInTransaction(db.transaction())
    background = BackgroundTask(
        onParsingRegistry,
        snapshotId=snapshot.get("id"),
        registryId=registryId,
        type=snapshot.get("type"),
    )
    return JSONResponse(dict(payload=payload), background=background)
