from starlette.requests import Request
from src.utils.sessions import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    ensureUserHasPermission,
)
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.IdentityAndAccessManaging.application.queries.RetrievePermission import (
    RetrievePermission,
)
from dataclasses import asdict


async def onRetrievingPermission(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request, mustBeOwner=True)
    permissionId = request.path_params.get("permissionId")
    db = client()
    payload = dict()
    retrievePermission = RetrievePermission(db=db)
    permission = await retrievePermission(credentials.uid, tenant.id, permissionId)
    payload.update(permission=asdict(permission))
    return JSONResponse(dict(payload=payload))
