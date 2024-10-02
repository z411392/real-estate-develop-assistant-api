from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Coroutine
from src.utils.sessions import withCredentials
from firebase_admin.firestore_async import client
from src.modules.TenantManaging.application.mutations.ResolveTeant import (
    ResolveTenant,
)
from src.utils.sessions import SessionKeys


class withTenantResolving(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Coroutine[None, None, Response]],
    ):
        credentials = withCredentials(request)
        if credentials is None:
            response = await call_next(request)
            return response

        tenantId: str = request.path_params.get("tenantId")
        db = client()
        resolveTenant = ResolveTenant(db=db)
        tenant = await resolveTenant(credentials.get("uid"), tenantId)
        if tenant:
            request.scope[SessionKeys.Tenant] = tenant
        response = await call_next(request)
        return response
