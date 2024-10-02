from starlette.requests import Request
from src.utils.sessions import ensureUserIsAuthenticated
from firebase_admin.firestore_async import client
from src.modules.TenantManaging.application.queries.CountTenants import (
    CountingTenants,
    CountTenants,
)
from starlette.responses import Response
from marshmallow import Schema


def _createValidator():
    Validator = Schema.from_dict(dict())
    validator = Validator()
    return validator


async def _createQuery(request: Request):
    validator = _createValidator()
    query = CountingTenants(**validator.load(dict(**request.query_params)))
    return query


async def onCountingTenants(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    query = await _createQuery(request)
    db = client()
    countTenants = CountTenants(db=db)
    count = await countTenants(credentials.get("uid"), query)
    response = Response()
    response.headers["content-length"] = str(count)
    return response
