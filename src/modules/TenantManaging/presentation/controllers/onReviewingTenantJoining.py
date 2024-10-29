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
from marshmallow import Schema
from marshmallow.fields import String
from marshmallow.validate import OneOf
from src.modules.IdentityAndAccessManaging.dtos.PermissionStatuses import (
    PermissionStatuses,
)


def createSchema():
    MutationSchema = Schema.from_dict(
        {
            "permissionId": String(required=True),
            "status": String(
                validate=OneOf(
                    [str(PermissionStatuses.Approved), str(PermissionStatuses.Rejected)]
                ),
                required=True,
            ),
        }
    )
    schema: Schema = MutationSchema()
    return schema


async def onReviewingTenantJoining(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    permission = ensureUserHasPermission(request, mustBeOwner=True)
    schema = createSchema()
    mutation = ReviewingTenantJoining(
        **schema.load(
            dict(
                **await request.json(),
                permissionId=request.path_params.get("permissionId")
            )
        )
    )
    db = client()
    payload = dict()
    if permission.id == mutation.permissionId:
        return JSONResponse(dict(payload=payload))
    async with Transaction(db) as transaction:
        payload.update(permissionId=mutation.permissionId)
        reviewTenantJoining = ReviewTenantJoining(db=db, transaction=transaction)
        await reviewTenantJoining(credentials.uid, tenant.id, mutation)
    return JSONResponse(dict(payload=payload))
