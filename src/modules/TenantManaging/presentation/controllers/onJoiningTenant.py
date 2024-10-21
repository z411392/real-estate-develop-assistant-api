from starlette.requests import Request
from src.utils.session import ensureUserIsAuthenticated
from starlette.responses import JSONResponse
from src.utils.session import ensureTenantIsSpecified
from firebase_admin.firestore_async import client
from src.modules.TenantManaging.application.mutations.JoinTenant import JoinTenant


async def onJoiningTenant(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    db = client()
    payload = dict()
    async with db.transaction() as transaction:
        joinTenant = JoinTenant(db=db, transaction=transaction)
        permissionId = await joinTenant(credentials.uid, tenant.id)
        payload.update(permissionId=permissionId)
    return JSONResponse(dict(payload=payload))
