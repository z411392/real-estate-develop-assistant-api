from starlette.requests import Request
from src.utils.sessions import ensureUserIsAuthenticated, ensureTenantIsSpecified, ensureUserHasPermission, ensureUserHasOwnership
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.SnapshotManaging.dtos.ListingRegistries import ListingRegistries
from src.modules.SnapshotManaging.application.queries.ListRegistries import ListRegistries
from dataclasses import asdict


async def onListingRegistries(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    ownership = ensureUserHasOwnership(request)
    query = await ListingRegistries.fromRequest(request)
    db = client()
    listRegistries = ListRegistries(db=db)
    registries = []
    async for registry in listRegistries(credentials.uid, tenant.id, ownership.resourceId, query):
        registries.append(asdict(registry))
    payload = dict(registries=registries)
    return JSONResponse(dict(payload=payload))
