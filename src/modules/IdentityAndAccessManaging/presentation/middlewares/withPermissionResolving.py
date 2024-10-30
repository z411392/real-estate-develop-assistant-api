from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Coroutine
from src.utils.sessions import withCredentials
from firebase_admin.firestore_async import client
from src.modules.IdentityAndAccessManaging.application.mutations.ResolvePermission import (
    ResolvePermission,
)
from src.utils.sessions import SessionKeys


class withPermissionResolving(BaseHTTPMiddleware):
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
        resolvePermission = ResolvePermission(db=db)
        pair = await resolvePermission(credentials.uid, tenantId)
        if pair is None:
            response = await call_next(request)
            return response

        tenant, permission = pair
        request.scope[SessionKeys.Tenant] = tenant
        request.scope[SessionKeys.Permission] = permission
        response = await call_next(request)
        return response
