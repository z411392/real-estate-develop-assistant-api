from starlette.requests import Request
from src.utils.sessions import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    ensureUserHasPermission,
    ensureSnapshotIsSpecified,
)
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.RegistryManaging.application.queries.RetrieveRegistry import (
    RetrieveRegistry,
)
from src.modules.RegistryManaging.presentation.transformers.FromRegistryToRegistryDisplayedTransformer import (
    FromRegistryToRegistryDisplayedTransformer,
)
from src.adapters.firestore.RegistryFragmentDao import RegistryFragmentDao


async def onRetrievingRegistry(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    snapshot = ensureSnapshotIsSpecified(request)
    registryId = request.path_params.get("registryId")
    db = client()
    registryFragmentDao = RegistryFragmentDao(db=db)
    payload = dict()
    retrieveRegistry = RetrieveRegistry(db=db)
    registry = await retrieveRegistry(
        credentials.get("uid"), tenant.get("id"), snapshot.get("id"), registryId
    )
    fragments = registryFragmentDao.all(snapshot.get("id"), registry.get("id"))
    transformer = FromRegistryToRegistryDisplayedTransformer(registry.get("type"))
    transformed = await transformer(registry, fragments)
    payload.update(registry=transformed)
    return JSONResponse(dict(payload=payload))
