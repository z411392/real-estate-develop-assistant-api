from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Coroutine
from src.utils.sessions import withCredentials, withTenant
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
        tenant = withTenant(request)
        if tenant is None:
            response = await call_next(request)
            return response
        db = client()
        resolvePermission = ResolvePermission(db=db)
        permission = await resolvePermission(credentials.get("uid"), tenant.get("id"))
        if permission:
            request.scope[SessionKeys.Permission] = permission
        response = await call_next(request)
        return response
