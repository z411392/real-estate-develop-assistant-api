from marshmallow import Schema
from marshmallow import fields
from starlette.requests import Request
from dataclasses import dataclass
from typing import List


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


@dataclass
class LandDescriptor:
    city: str
    administrativeDistrict: str
    section: str
    subsection: str
    parentLotNumber: str
    subLotNumber: str


@dataclass
class RetrievingLands:
    landDescriptors: List[LandDescriptor]

    @staticmethod
    async def fromRequest(request: Request):
        schema = createSchema()
        data = schema.load(dict(**await request.json()))
        landDescriptors = (
            [
                LandDescriptor(**landDescriptor)
                for landDescriptor in data.get("landDescriptors")
            ]
            if data.get("landDescriptors")
            else []
        )
        return RetrievingLands(landDescriptors=landDescriptors)
