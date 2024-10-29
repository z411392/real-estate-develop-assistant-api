from starlette.requests import Request
from src.utils.sessions import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    ensureUserHasPermission,
    ensureUserHasOwnership,
)
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.SnapshotManaging.application.queries.RetrieveRegistry import (
    RetrieveRegistry,
)
from dataclasses import asdict


async def onRetrievingRegistry(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    ensureUserHasOwnership(request)
    snapshotId = request.path_params.get("snapshotId")
    registryId = request.path_params.get("registryId")
    db = client()
    payload = dict()
    retrieveRegistry = RetrieveRegistry(db=db)
    registry = await retrieveRegistry(credentials.uid, tenant.id, snapshotId, registryId)
    payload.update(registry=asdict(registry))
    return JSONResponse(dict(payload=payload))
