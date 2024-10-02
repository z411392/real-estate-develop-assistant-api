from starlette.requests import Request
from src.utils.session import ensureUserIsAuthenticated, ensureTenantIsSpecified, ensureUserHasPermission, ensureUserHasOwnership
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.SnapshotManaging.application.mutations.ParseRegistry import ParseRegistry


async def onParsingRegistry(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    ensureUserHasOwnership(request)
    snapshotId = request.path_params.get("snapshotId")
    registryId = request.path_params.get("registryId")
    db = client()
    payload = dict()
    async with db.transaction() as transaction:
        parseRegistry = ParseRegistry(db=db, transaction=transaction)
        registry = await parseRegistry(credentials.uid, tenant.id, snapshotId, registryId)
        payload.update(registryId=registry.id)
    return JSONResponse(dict(payload=payload))
