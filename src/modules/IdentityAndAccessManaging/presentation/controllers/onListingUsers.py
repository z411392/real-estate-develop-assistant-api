from starlette.requests import Request
from src.utils.sessions import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    ensureUserHasPermission,
)
from firebase_admin.firestore_async import client
from src.modules.IdentityAndAccessManaging.application.queries.ListUsers import (
    ListUsers,
)
from starlette.responses import JSONResponse
from src.modules.IdentityAndAccessManaging.dtos.ListingUsers import ListingUsers
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


async def onListingUsers(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request, mustBeOwner=True)
    schema = createSchema()
    query = ListingUsers(**schema.load(dict(**request.query_params)))
    db = client()
    listUsers = ListUsers(db=db)
    users = []
    async for user, permission in listUsers(credentials.uid, tenant.id, query):
        users.append(dict(**asdict(user), permission=asdict(permission)))
    payload = dict(users=users)
    return JSONResponse(dict(payload=payload))
