from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Coroutine
from src.utils.sessions import ensureUserIsAuthenticated, ensureTenantIsSpecified, ensureUserHasPermission
from src.modules.SnapshotManaging.application.mutations.ResolveSnapshot import ResolveSnapshot
from firebase_admin.firestore_async import client
from src.utils.sessions import SessionKeys


class withSnapshotResolving(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Coroutine[None, None, Response]],
    ):
        credentials = ensureUserIsAuthenticated(request)
        tenant = ensureTenantIsSpecified(request)
        ensureUserHasPermission(request)
        snapshotId = request.path_params.get("snapshotId")
        db = client()
        resolveSnapshot = ResolveSnapshot(db=db)
        snapshot = await resolveSnapshot(credentials.get("uid"), tenant.get("id"), snapshotId)
        request.scope[SessionKeys.Snapshot] = snapshot
        response = await call_next(request)
        return response
