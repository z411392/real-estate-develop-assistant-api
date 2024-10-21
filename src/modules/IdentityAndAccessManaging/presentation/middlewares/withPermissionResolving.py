from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Coroutine
from src.utils.session import withCredentials
from firebase_admin.firestore_async import client
from src.modules.IdentityAndAccessManaging.application.mutations.ResolvePermission import ResolvePermission
from src.utils.session import SessionKeys


class withPermissionResolving(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Coroutine[None, None, Response]],
    ):
        tenantId = request.path_params.get("tenantId")
        if tenantId is not None:
            credentials = withCredentials(request)
            if credentials is not None:
                db = client()
                resolvePermission = ResolvePermission(db=db)
                pair = await resolvePermission(credentials.uid, tenantId)
                if pair is not None:
                    tenant, permission = pair
                    request.scope[SessionKeys.Tenant] = tenant
                    request.scope[SessionKeys.Permission] = permission
        response = await call_next(request)
        return response
