from starlette.requests import Request
from src.utils.session import ensureUserIsAuthenticated
from starlette.responses import JSONResponse
from src.utils.session import ensureTenantIsSpecified, ensureUserHasPermission
from firebase_admin.firestore_async import client
from src.modules.TenantManaging.application.mutations.JoinTenant import JoinTenant
from src.modules.TenantManaging.dtos.JoiningTenant import JoiningTenant


async def onJoiningTenant(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request, mustBeOwner=True)
    mutation = await JoiningTenant.fromRequest(request)
    db = client()
    payload = dict()
    async with db.transaction() as transaction:
        joinTenant = JoinTenant(db=db, transaction=transaction)
        permissionId = await joinTenant(credentials.uid, tenant.id, mutation)
        payload.update(permissionId=permissionId)
    return JSONResponse(dict(payload=payload))
