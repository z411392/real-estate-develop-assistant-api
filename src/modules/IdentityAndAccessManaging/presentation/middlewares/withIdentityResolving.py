from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Coroutine
import re
from src.modules.IdentityAndAccessManaging.application.mutations.ResolveCredentials import ResolveCredentials
from src.modules.IdentityAndAccessManaging.dtos.Credentials import Credentials
from src.utils.sessions import SessionKeys
from typing import Optional


class withIdentityResolving(BaseHTTPMiddleware):
    def _retrieveTokenFromAuthorizationHeader(self, request: Request):
        authorization: Optional[str] = request.headers.get("Authorization")
        if authorization is None:
            return None
        split = re.split(r'bearer\s+', authorization, flags=re.IGNORECASE)
        if len(split) == 0:
            return None
        token: Optional[str] = str.strip(
            split[1]) if split[1] is not None else None
        if token is None:
            return None
        return token

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Coroutine[None, None, Response]],
    ):
        token: Optional[str] = self._retrieveTokenFromAuthorizationHeader(
            request)
        if token:
            resolveCredentialsFromJsonWebToken = ResolveCredentials()
            credentials: Credentials = await resolveCredentialsFromJsonWebToken(token)
            if credentials is not None:
                request.scope[SessionKeys.Credentials] = credentials
        response = await call_next(request)
        return response
