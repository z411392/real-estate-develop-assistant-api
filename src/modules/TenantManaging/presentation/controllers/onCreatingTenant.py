from starlette.requests import Request
from src.utils.sessions import ensureUserIsAuthenticated
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.TenantManaging.dtos.CreatingTenant import CreatingTenant
from src.modules.TenantManaging.application.mutations.CreateTenant import CreateTenant
from src.utils.firestore import Transaction

from marshmallow import Schema
from marshmallow.fields import String
from marshmallow.validate import Length


def createSchema():
    MutationSchema = Schema.from_dict({
        "name": String(validate=Length(1, 15), required=True),
    })
    schema: Schema = MutationSchema()
    return schema


async def onCreatingTenant(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    schema = createSchema()
    mutation = CreatingTenant(**schema.load(dict(**await request.json())))
    db = client()
    payload = dict()
    async with Transaction(db) as transaction:
        createTenant = CreateTenant(db=db, transaction=transaction)
        tenantId = await createTenant(credentials.uid, mutation)
        payload.update(tenantId=tenantId)
    return JSONResponse(dict(payload=payload))
