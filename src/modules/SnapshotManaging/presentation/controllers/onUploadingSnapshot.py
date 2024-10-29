from starlette.requests import Request
from starlette.responses import JSONResponse
from src.modules.SnapshotManaging.application.mutations.UploadSnapshot import UploadSnapshot
from src.utils.sessions import ensureUserIsAuthenticated, ensureTenantIsSpecified, ensureUserHasPermission
from firebase_admin.firestore_async import client
from src.modules.SnapshotManaging.dtos.UploadingSnapshot import UploadingSnapshot
from src.utils.firestore import Transaction
from marshmallow import Schema
from marshmallow.fields import String


def createSchema():
    MutationSchema = Schema.from_dict({
        "name": String(),
        "content": String(),
    })
    schema: Schema = MutationSchema()
    return schema


async def onUploadingSnapshot(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    schema = createSchema()
    mutation = UploadingSnapshot(**schema.load(dict(**await request.json())))
    db = client()
    payload = dict()
    async with Transaction(db) as transaction:
        uploadSnapshot = UploadSnapshot(db=db, transaction=transaction)
        snapshotId = await uploadSnapshot(credentials.uid, tenant.id, mutation)
        payload.update(snapshotId=snapshotId)
    return JSONResponse(dict(payload=payload))
