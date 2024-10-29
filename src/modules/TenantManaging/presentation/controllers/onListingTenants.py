from starlette.requests import Request
from src.utils.sessions import ensureUserIsAuthenticated
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.TenantManaging.dtos.ListingTenants import ListingTenants
from src.modules.TenantManaging.application.queries.ListTenants import ListTenants
from dataclasses import asdict
from marshmallow import Schema
from marshmallow.fields import Integer
from marshmallow.validate import Range


def createSchema():
    QuerySchema = Schema.from_dict({
        "page": Integer(validate=Range(min=1), missing=1),
    })
    schema: Schema = QuerySchema()
    return schema


async def onListingTenants(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    schema = createSchema()
    query = ListingTenants(**schema.load(dict(**request.query_params)))
    db = client()
    listTenants = ListTenants(db=db)
    tenants = []
    async for tenant in listTenants(credentials.uid, query):
        tenants.append(asdict(tenant))
    payload = dict(tenants=tenants)
    return JSONResponse(dict(payload=payload))
