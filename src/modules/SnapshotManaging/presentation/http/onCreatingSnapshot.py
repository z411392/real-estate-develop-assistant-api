from starlette.requests import Request
from starlette.responses import JSONResponse
from src.utils.storage import filePathFor
from src.modules.SnapshotManaging.errors.MustBeInPDFFormat import MustBeInPDFFormat
from src.modules.SnapshotManaging.application.mutations.CreateSnapshot import CreateSnapshot
from src.utils.session import ensureUserIsAuthenticated, ensureTenantIsSpecified, ensureUserHasPermission
from firebase_admin.firestore_async import client


async def onCreatingSnapshot(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    buffer = await request.body()
    filePath = filePathFor(buffer)
    if not filePath.startswith("pdf"):
        raise MustBeInPDFFormat()
    payload = dict()
    db = client()
    async with db.transaction() as transaction:
        createRegistry = CreateSnapshot(db=db, transaction=transaction)
        snapshotId = await createRegistry(credentials.uid, tenant.id, filePath, buffer)
        payload.update(snapshotId=snapshotId)
    return JSONResponse(dict(payload=payload))
