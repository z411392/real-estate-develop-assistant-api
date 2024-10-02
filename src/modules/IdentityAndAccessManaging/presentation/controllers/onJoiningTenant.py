from starlette.requests import Request
from src.utils.sessions import ensureUserIsAuthenticated
from starlette.responses import JSONResponse
from src.utils.sessions import ensureTenantIsSpecified
from firebase_admin.firestore_async import client
from src.modules.IdentityAndAccessManaging.application.mutations.JoinTenant import (
    JoinTenant,
)
from google.cloud.firestore import async_transactional


async def onJoiningTenant(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    db = client()
    payload = dict()

    @async_transactional
    async def runInTransaction(transaction):
        joinTenant = JoinTenant(db=db, transaction=transaction)
        permissionId = await joinTenant(credentials.get("uid"), tenant.get("id"))
        payload.update(permissionId=permissionId)

    await runInTransaction(db.transaction())

    return JSONResponse(dict(payload=payload))
