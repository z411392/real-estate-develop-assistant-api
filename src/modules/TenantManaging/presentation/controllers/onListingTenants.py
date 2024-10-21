from starlette.requests import Request
from src.utils.session import ensureUserIsAuthenticated
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.TenantManaging.dtos.ListingTenants import ListingTenants
from src.modules.TenantManaging.application.queries.ListTenants import ListTenants
from dataclasses import asdict


async def onListingTenants(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    query = await ListingTenants.fromRequest(request)
    db = client()
    listTenants = ListTenants(db=db)
    tenants = []
    async for tenant in listTenants(credentials.uid, query):
        tenants.append(asdict(tenant))
    payload = dict(tenants=tenants)
    return JSONResponse(dict(payload=payload))
