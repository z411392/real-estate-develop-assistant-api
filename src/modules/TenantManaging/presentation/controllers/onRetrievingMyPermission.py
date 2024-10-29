from starlette.requests import Request
from src.utils.sessions import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    withPermission,
)
from starlette.responses import JSONResponse
from dataclasses import asdict


async def onRetrievingMyPermission(request: Request):
    ensureUserIsAuthenticated(request)
    ensureTenantIsSpecified(request)
    permission = withPermission(request)
    payload = dict(permission=asdict(permission) if permission else None)
    return JSONResponse(dict(payload=payload))
