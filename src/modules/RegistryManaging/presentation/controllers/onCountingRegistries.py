from starlette.requests import Request
from src.utils.sessions import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    ensureUserHasPermission,
    ensureSnapshotIsSpecified,
)
from firebase_admin.firestore_async import client
from src.modules.RegistryManaging.application.queries.CountRegistries import (
    CountingRegistries,
    CountRegistries,
)
from starlette.responses import Response
from marshmallow import Schema


def _createValidator():
    Validator = Schema.from_dict({})
    validator = Validator()
    return validator


async def _createQuery(request: Request):
    validator = _createValidator()
    query = CountingRegistries(**validator.load(dict(**request.query_params)))
    return query


async def onCountingRegistries(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    snapshot = ensureSnapshotIsSpecified(request)
    query = await _createQuery(request)
    db = client()
    countRegistries = CountRegistries(db=db)
    count = await countRegistries(
        credentials.get("uid"), tenant.get("id"), snapshot.get("id"), query
    )
    response = Response()
    response.headers["content-length"] = str(count)
    return response
