from starlette.requests import Request
from src.utils.session import ensureUserIsAuthenticated, ensureTenantIsSpecified, ensureUserHasPermission, ensureUserHasOwnership
from firebase_admin.firestore_async import client
from src.modules.SnapshotManaging.application.queries.CountRegistries import CountRegistries
from starlette.responses import Response


async def onCountingRegistries(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    ownership = ensureUserHasOwnership(request)
    db = client()
    countRegistries = CountRegistries(db=db)
    count = await countRegistries(credentials.uid, tenant.id, ownership.resourceId)
    response = Response()
    response.headers["content-length"] = str(count)
    return response
