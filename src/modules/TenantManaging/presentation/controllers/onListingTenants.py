from starlette.requests import Request
from src.utils.sessions import ensureUserIsAuthenticated
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.TenantManaging.application.queries.ListTenants import (
    ListingTenants,
    ListTenants,
)
from marshmallow import Schema
from src.utils.validators import (
    page,
)


def _createValidator():
    Validator = Schema.from_dict(dict(page=page))
    validator = Validator()
    return validator


async def _createQuery(request: Request):
    validator = _createValidator()
    query = ListingTenants(**validator.load(dict(**request.query_params)))
    return query


async def onListingTenants(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    query = await _createQuery(request)
    db = client()
    listTenants = ListTenants(db=db)
    tenants = []
    async for tenant in listTenants(credentials.get("uid"), query):
        tenants.append(tenant)
    payload = dict(tenants=tenants)
    return JSONResponse(dict(payload=payload))
