from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Coroutine
from src.constants import Collections
from src.utils.session import ensureUserIsAuthenticated, ensureTenantIsSpecified, ensureUserHasPermission
from src.modules.IdentityAndAccessManaging.application.mutations.ResolveSnapshotOwnership import ResolveSnapshotOwnership
from firebase_admin.firestore_async import client
from src.utils.session import SessionKeys


class withSnapshotOwnershipResolving(BaseHTTPMiddleware):

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
        resolveSnapshotOwnership = ResolveSnapshotOwnership(db=db)
        ownership = await resolveSnapshotOwnership(credentials.uid, tenant.id, snapshotId)
        request.scope[SessionKeys.Ownership] = ownership
        response = await call_next(request)
        return response
