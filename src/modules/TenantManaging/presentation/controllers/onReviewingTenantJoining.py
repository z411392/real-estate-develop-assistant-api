from starlette.requests import Request
from src.utils.session import ensureUserIsAuthenticated, ensureTenantIsSpecified, ensureUserHasPermission
from starlette.responses import JSONResponse
from src.modules.TenantManaging.dtos.ReviewingTenantJoining import ReviewingTenantJoining
from firebase_admin.firestore_async import client
from src.modules.TenantManaging.application.mutations.ReviewTenantJoining import ReviewTenantJoining


async def onReviewingTenantJoining(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request, mustBeOwner=True)
    mutation = await ReviewingTenantJoining.fromRequest(request)
    db = client()
    payload = dict()
    async with db.transaction() as transaction:
        reviewTenantJoining = ReviewTenantJoining(db=db, transaction=transaction)
        permissionId = await reviewTenantJoining(credentials.uid, tenant.id, mutation)
        payload.update(permissionId=permissionId)
    return JSONResponse(dict(payload=payload))
