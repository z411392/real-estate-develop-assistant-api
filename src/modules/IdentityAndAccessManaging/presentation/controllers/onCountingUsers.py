from starlette.requests import Request
from src.utils.sessions import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    ensureUserHasPermission,
)
from firebase_admin.firestore_async import client
from src.modules.IdentityAndAccessManaging.application.queries.CountUsers import (
    CountingUsers,
    CountUsers,
)
from starlette.responses import Response
from marshmallow import Schema
from src.constants import Root


def _createValidator():
    Validator = Schema.from_dict({})
    validator = Validator()
    return validator


async def _createQuery(request: Request):
    validator = _createValidator()
    query = CountingUsers(**validator.load(dict(**request.query_params)))
    return query


async def onCountingUsers(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    if credentials.get("uid") != Root:
        ensureUserHasPermission(request, mustBeOwner=True)
    query = await _createQuery(request)
    db = client()
    countUsers = CountUsers(db=db)
    count = await countUsers(credentials.get("uid"), tenant.get("id"), query)
    response = Response()
    response.headers["content-length"] = str(count)
    return response
