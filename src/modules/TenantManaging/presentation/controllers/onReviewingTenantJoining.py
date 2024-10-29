from starlette.requests import Request
from src.utils.sessions import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    ensureUserHasPermission,
)
from starlette.responses import JSONResponse
from src.modules.TenantManaging.dtos.ReviewingTenantJoining import (
    ReviewingTenantJoining,
)
from firebase_admin.firestore_async import client
from src.modules.TenantManaging.application.mutations.ReviewTenantJoining import (
    ReviewTenantJoining,
)
from src.utils.firestore import Transaction


async def onReviewingTenantJoining(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    permission = ensureUserHasPermission(request, mustBeOwner=True)
    mutation = await ReviewingTenantJoining.fromRequest(request)
    db = client()
    payload = dict()
    if permission.id == mutation.permissionId:
        return JSONResponse(dict(payload=payload))
    async with Transaction(db) as transaction:
        payload.update(permissionId=mutation.permissionId)
        reviewTenantJoining = ReviewTenantJoining(db=db, transaction=transaction)
        await reviewTenantJoining(credentials.uid, tenant.id, mutation)
    return JSONResponse(dict(payload=payload))
