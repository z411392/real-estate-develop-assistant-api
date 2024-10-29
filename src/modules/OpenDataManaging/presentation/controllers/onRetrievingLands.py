from starlette.requests import Request
from src.utils.sessions import ensureUserIsAuthenticated, ensureTenantIsSpecified
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.OpenDataManaging.dtos.LandDescriptor import LandDescriptor
from src.modules.OpenDataManaging.dtos.RetrievingLands import RetrievingLands
from src.modules.OpenDataManaging.application.queries.RetrieveLands import RetrieveLands
from dataclasses import asdict
from marshmallow import Schema
from marshmallow import fields


def createSchema():
    LandDescriptorSchema = Schema.from_dict(
        dict(
            city=fields.String(),
            administrativeDistrict=fields.String(),
            section=fields.String(),
            subsection=fields.String(),
            parentLotNumber=fields.String(),
            subLotNumber=fields.String(),
        )
    )
    QuerySchema = Schema.from_dict(
        dict(
            landDescriptors=fields.List(fields.Nested(LandDescriptorSchema())),
        )
    )
    schema: Schema = QuerySchema()
    return schema


async def onRetrievingLands(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    schema = createSchema()
    data = schema.load(dict(**await request.json()))
    query = RetrievingLands(
        landDescriptors=(
            [
                LandDescriptor(**landDescriptor)
                for landDescriptor in data.get("landDescriptors")
            ]
            if data.get("landDescriptors")
            else []
        )
    )
    db = client()
    retrieveLands = RetrieveLands(db=db)
    lands = []
    async for land in retrieveLands(credentials.uid, tenant.id, query):
        lands.append(asdict(land))
    payload = dict(lands=lands)
    return JSONResponse(dict(payload=payload))
