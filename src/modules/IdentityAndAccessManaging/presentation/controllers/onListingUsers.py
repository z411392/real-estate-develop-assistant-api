from starlette.requests import Request
from src.utils.sessions import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    ensureUserHasPermission,
)
from firebase_admin.firestore_async import client
from src.modules.IdentityAndAccessManaging.application.queries.ListUsers import (
    ListUsers,
    ListingUsers,
)
from starlette.responses import JSONResponse
from marshmallow import Schema
from src.utils.validators import page
from src.constants import Root


def _createValidator():
    Validator = Schema.from_dict(
        dict(
            page=page,
        ),
    )
    validator = Validator()
    return validator


async def _createQuery(request: Request):
    validator = _createValidator()
    query = ListingUsers(**validator.load(dict(**request.query_params)))
    return query


async def onListingUsers(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    if credentials.get("uid") != Root:
        ensureUserHasPermission(request, mustBeOwner=True)
    query = await _createQuery(request)
    db = client()
    listUsers = ListUsers(db=db)
    users = []
    async for user, permission in listUsers(
        credentials.get("uid"), tenant.get("id"), query
    ):
        users.append(dict(**user, permission=permission))
    payload = dict(users=users)
    return JSONResponse(dict(payload=payload))
