from dataclasses import dataclass
from marshmallow import Schema
from marshmallow.fields import Integer
from marshmallow.validate import Range
from starlette.requests import Request


def createSchema():
    QuerySchema = Schema.from_dict({
        "page": Integer(validate=Range(min=1), missing=1),
    })
    schema: Schema = QuerySchema()
    return schema


@dataclass
class ListingUsers:
    page: int

    @staticmethod
    async def fromRequest(request: Request):
        schema = createSchema()
        return ListingUsers(**schema.load(dict(**request.query_params)))
