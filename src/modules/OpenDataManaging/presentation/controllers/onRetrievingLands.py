from starlette.requests import Request
from src.utils.sessions import ensureUserIsAuthenticated, ensureTenantIsSpecified
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.OpenDataManaging.application.queries.RetrieveLands import (
    RetrieveLands,
    RetrievingLands,
)
from marshmallow import Schema
from src.modules.OpenDataManaging.presentation.validators.LandDescriptor import (
    landDescriptors,
)


def _createValidator():
    Validator = Schema.from_dict(
        dict(
            landDescriptors=landDescriptors,
        )
    )
    validator = Validator()
    return validator


async def _createQuery(request: Request):
    validator = _createValidator()
    query = RetrievingLands(**validator.load(dict(**await request.json())))
    return query


async def onRetrievingLands(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    query = await _createQuery(request)
    db = client()
    retrieveLands = RetrieveLands(db=db)
    lands = []
    async for land in retrieveLands(credentials.get("uid"), tenant.get("id"), query):
        lands.append(land)
    payload = dict(lands=lands)
    return JSONResponse(dict(payload=payload))
