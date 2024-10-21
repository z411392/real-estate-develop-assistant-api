from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Coroutine
from src.constants import Collections
from src.utils.session import ensureUserIsAuthenticated, ensureTenantIsSpecified, ensureUserHasPermission
from src.modules.IdentityAndAccessManaging.application.quries.ResolveOwnership import ResolveOwnership
from firebase_admin.firestore_async import client
from src.utils.session import SessionKeys


class withOwnershipResolving(BaseHTTPMiddleware):
    _resourceType: str

    def __init__(self, app, resourceType: str):
        super().__init__(app)
        self._resourceType = resourceType

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Coroutine[None, None, Response]],
    ):
        if self._resourceType == str(Collections.Snapshots):
            credentials = ensureUserIsAuthenticated(request)
            tenant = ensureTenantIsSpecified(request)
            ensureUserHasPermission(request)
            snapshotId = request.path_params.get("snapshotId")
            db = client()
            resolveOwnership = ResolveOwnership(db=db)
            ownership = await resolveOwnership(credentials.uid, tenant.id, snapshotId)
            request.scope[SessionKeys.Ownership] = ownership
        response = await call_next(request)
        return response
