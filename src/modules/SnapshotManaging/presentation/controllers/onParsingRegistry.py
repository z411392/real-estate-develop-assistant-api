from starlette.requests import Request
from src.utils.session import ensureUserIsAuthenticated, ensureTenantIsSpecified, ensureUserHasPermission, ensureUserHasOwnership
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.SnapshotManaging.application.mutations.ParseRegistry import ParseRegistry
from src.utils.firestore import Transaction
from src.modules.CreditManaging.application.mutations.UseCredits import UseCredits


async def onParsingRegistry(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    ensureUserHasOwnership(request)
    snapshotId = request.path_params.get("snapshotId")
    registryId = request.path_params.get("registryId")
    db = client()
    payload = dict()
    creditsToBeUsed = 1
    async with Transaction(db) as transaction:
        useCredits = UseCredits(db=db, transaction=transaction)
        await useCredits(credentials.uid, tenant.id, creditsToBeUsed=creditsToBeUsed)
    async with Transaction(db) as transaction:
        parseRegistry = ParseRegistry(db=db, transaction=transaction)
        await parseRegistry(credentials.uid, tenant.id, snapshotId, registryId)
        payload.update(registryId=registryId)
    return JSONResponse(dict(payload=payload))
