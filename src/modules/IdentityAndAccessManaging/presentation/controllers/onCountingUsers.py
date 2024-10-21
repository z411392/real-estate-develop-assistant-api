from starlette.requests import Request
from src.utils.session import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    ensureUserHasPermission,
)
from firebase_admin.firestore_async import client
from src.modules.IdentityAndAccessManaging.application.queries.CountUsers import CountUsers
from starlette.responses import Response


async def onCountingUsers(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request, mustBeOwner=True)
    db = client()
    countUsers = CountUsers(db=db)
    count = await countUsers(credentials.uid, tenant.id)
    response = Response()
    response.headers["content-length"] = str(count)
    return response
