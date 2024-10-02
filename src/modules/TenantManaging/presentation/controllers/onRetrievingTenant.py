from starlette.requests import Request
from src.utils.sessions import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    withPermission,
)
from starlette.responses import JSONResponse


async def onRetrievingTenant(request: Request):
    ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    permission = withPermission(request)
    payload = dict(
        tenant=tenant,
        permission=permission,
    )
    return JSONResponse(dict(payload=payload))
