from starlette.requests import Request
from src.utils.session import ensureUserIsAuthenticated, ensureTenantIsSpecified, ensureUserHasPermission, ensureUserHasOwnership
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.SnapshotManaging.application.queries.RetrieveSnapshot import RetrieveSnapshot
from dataclasses import asdict


async def onRetrievingSnapshot(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    ensureUserHasOwnership(request)
    snapshotId = request.path_params.get("snapshotId")
    db = client()
    payload = dict()
    retrieveSnapshot = RetrieveSnapshot(db=db)
    snapshot = await retrieveSnapshot(credentials.uid, tenant.id, snapshotId)
    payload.update(snapshot=asdict(snapshot))
    return JSONResponse(dict(payload=payload))
