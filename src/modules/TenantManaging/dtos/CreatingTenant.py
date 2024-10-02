from dataclasses import dataclass
from marshmallow import Schema
from marshmallow.fields import String
from marshmallow.validate import Length
from starlette.requests import Request


def createSchema():
    MutationSchema = Schema.from_dict({
        "name": String(validate=Length(1, 15), required=True),
    })
    schema: Schema = MutationSchema()
    return schema


@dataclass
class CreatingTenant:
    name: str

    @staticmethod
    async def fromRequest(request: Request):
        schema = createSchema()
        return CreatingTenant(**schema.load(dict(**await request.json())))
