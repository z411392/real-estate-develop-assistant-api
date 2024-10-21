from starlette.requests import Request
from src.utils.session import ensureUserIsAuthenticated
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.TenantManaging.dtos.CreatingTenant import CreatingTenant
from src.modules.TenantManaging.application.mutations.CreateTenant import CreateTenant


async def onCreatingTenant(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    mutation = await CreatingTenant.fromRequest(request)
    db = client()
    payload = dict()
    async with db.transaction() as transaction:
        createTenant = CreateTenant(db=db, transaction=transaction)
        tenantId = await createTenant(credentials.uid, mutation)
        payload.update(tenantId=tenantId)
    return JSONResponse(dict(payload=payload))
