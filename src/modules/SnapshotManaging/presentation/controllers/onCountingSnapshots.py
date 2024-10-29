from starlette.requests import Request
from src.utils.sessions import ensureUserIsAuthenticated, ensureTenantIsSpecified, ensureUserHasPermission
from firebase_admin.firestore_async import client
from src.modules.SnapshotManaging.application.queries.CountSnapshots import CountSnapshots
from starlette.responses import Response


async def onCountingSnapshots(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    db = client()
    countSnapshots = CountSnapshots(db=db)
    count = await countSnapshots(credentials.uid, tenant.id)
    response = Response()
    response.headers["content-length"] = str(count)
    return response
