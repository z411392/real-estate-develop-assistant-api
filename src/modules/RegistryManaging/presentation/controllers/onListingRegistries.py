from starlette.requests import Request
from src.utils.sessions import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    ensureUserHasPermission,
    ensureSnapshotIsSpecified,
)
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.RegistryManaging.application.queries.ListRegistries import (
    ListingRegistries,
    ListRegistries,
)
from marshmallow import Schema
from src.modules.RegistryManaging.presentation.transformers.FromRegistryToRegistryDisplayedTransformer import (
    FromRegistryToRegistryDisplayedTransformer,
)
from src.adapters.firestore.RegistryFragmentDao import RegistryFragmentDao


def _createValidator():
    Validator = Schema.from_dict({})
    validator = Validator()
    return validator


async def _createQuery(request: Request):
    validator = _createValidator()
    query = ListingRegistries(**validator.load(dict(**request.query_params)))
    return query


async def onListingRegistries(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    snapshot = ensureSnapshotIsSpecified(request)
    query = await _createQuery(request)
    db = client()
    registryFragmentDao = RegistryFragmentDao(db=db)
    listRegistries = ListRegistries(db=db)
    registries = []
    async for registry in listRegistries(
        credentials.get("uid"), tenant.get("id"), snapshot.get("id"), query
    ):
        transformer = FromRegistryToRegistryDisplayedTransformer(registry.get("type"))
        fragments = registryFragmentDao.all(snapshot.get("id"), registry.get("id"))
        transformed = await transformer(registry, fragments)
        registries.append(transformed)
    payload = dict(registries=registries)
    return JSONResponse(dict(payload=payload))
