from starlette.requests import Request
from src.utils.sessions import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    ensureUserHasPermission,
)
from firebase_admin.firestore_async import client
from src.modules.SnapshotManaging.application.queries.CountSnapshots import (
    CountingSnapshots,
    CountSnapshots,
)
from starlette.responses import Response
from marshmallow import Schema


def _createValidator():
    Validator = Schema.from_dict(dict())
    validator = Validator()
    return validator


async def _createQuery(request: Request):
    validator = _createValidator()
    query = CountingSnapshots(**validator.load(dict(**request.query_params)))
    return query


async def onCountingSnapshots(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    query = await _createQuery(request)
    db = client()
    countSnapshots = CountSnapshots(db=db)
    count = await countSnapshots(credentials.get("uid"), tenant.get("id"), query)
    response = Response()
    response.headers["content-length"] = str(count)
    return response
