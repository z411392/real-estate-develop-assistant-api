from starlette.requests import Request
from src.utils.sessions import ensureUserIsAuthenticated
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.TenantManaging.application.mutations.CreateTenant import (
    CreatingTenant,
    CreateTenant,
)
from marshmallow import Schema
from src.modules.TenantManaging.presentation.validators.Tenant import (
    name,
)
from google.cloud.firestore import async_transactional


def _createValidator():
    Validator = Schema.from_dict(dict(name=name))
    validator = Validator()
    return validator


async def _createMutation(request: Request):
    validator = _createValidator()
    mutation = CreatingTenant(**validator.load(dict(**await request.json())))
    return mutation


async def onCreatingTenant(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    mutation = await _createMutation(request)
    db = client()
    payload = dict()

    @async_transactional
    async def runInTransaction(transaction):
        createTenant = CreateTenant(db=db, transaction=transaction)
        tenantId = await createTenant(credentials.get("uid"), mutation)
        payload.update(tenantId=tenantId)

    await runInTransaction(db.transaction())

    return JSONResponse(dict(payload=payload))
