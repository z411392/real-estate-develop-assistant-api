from dataclasses import dataclass
from marshmallow import Schema
from starlette.requests import Request


def createSchema():
    QuerySchema = Schema.from_dict({})
    schema: Schema = QuerySchema()
    return schema


@dataclass
class ListingRegistries:

    @staticmethod
    async def fromRequest(request: Request):
        schema = createSchema()
        return ListingRegistries(**schema.load(dict(**request.query_params)))
