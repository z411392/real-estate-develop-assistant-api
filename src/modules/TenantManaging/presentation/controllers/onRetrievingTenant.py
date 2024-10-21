from starlette.requests import Request
from src.utils.session import ensureUserIsAuthenticated, ensureTenantIsSpecified
from starlette.responses import JSONResponse
from dataclasses import asdict


async def onRetrievingTenant(request: Request):
    ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    payload = dict(tenant=asdict(tenant))
    return JSONResponse(dict(payload=payload))
