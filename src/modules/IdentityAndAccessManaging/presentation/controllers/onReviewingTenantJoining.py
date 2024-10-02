from starlette.requests import Request
from src.utils.sessions import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    ensureUserHasPermission,
)
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.IdentityAndAccessManaging.application.mutations.ReviewTenantJoining import (
    ReviewingTenantJoining,
    ReviewTenantJoining,
)
from marshmallow import Schema
from src.modules.IdentityAndAccessManaging.presentation.validators.Permission import (
    permissionId,
    status,
)
from src.constants import Root
from typing import Optional
from src.modules.IdentityAndAccessManaging.dtos import Permission
from google.cloud.firestore import async_transactional
from operator import itemgetter


def _createValidator():
    Validator = Schema.from_dict(
        dict(
            permissionId=permissionId,
            status=status,
        ),
    )
    validator = Validator()
    return validator


async def _createMutation(request: Request):
    validator = _createValidator()
    mutation = ReviewingTenantJoining(
        **validator.load(
            dict(
                **await request.json(),
                permissionId=request.path_params.get("permissionId")
            )
        )
    )
    return mutation


async def onReviewingTenantJoining(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    permission: Optional[Permission] = None
    if credentials.get("uid") != Root:
        permission = ensureUserHasPermission(request, mustBeOwner=True)
    mutation = await _createMutation(request)
    permissionId = itemgetter("permissionId")(mutation)
    db = client()
    payload = dict()
    if permission and (permission.get("id") == permissionId):
        return JSONResponse(dict(payload=payload))

    @async_transactional
    async def runInTransaction(transaction):
        payload.update(permissionId=permissionId)
        reviewTenantJoining = ReviewTenantJoining(db=db, transaction=transaction)
        await reviewTenantJoining(credentials.get("uid"), tenant.get("id"), mutation)

    await runInTransaction(db.transaction())
    return JSONResponse(dict(payload=payload))
