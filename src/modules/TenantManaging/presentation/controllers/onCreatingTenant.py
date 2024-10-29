from starlette.requests import Request
from src.utils.sessions import ensureUserIsAuthenticated
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.TenantManaging.dtos.CreatingTenant import CreatingTenant
from src.modules.TenantManaging.application.mutations.CreateTenant import CreateTenant
from src.utils.firestore import Transaction


async def onCreatingTenant(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    mutation = await CreatingTenant.fromRequest(request)
    db = client()
    payload = dict()
    async with Transaction(db) as transaction:
        createTenant = CreateTenant(db=db, transaction=transaction)
        tenantId = await createTenant(credentials.uid, mutation)
        payload.update(tenantId=tenantId)
    return JSONResponse(dict(payload=payload))
