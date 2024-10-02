from dataclasses import dataclass
from marshmallow import Schema
from marshmallow.fields import String
from starlette.requests import Request


def createSchema():
    QuerySchema = Schema.from_dict({
        "userId": String(),
    })
    schema: Schema = QuerySchema()
    return schema


@dataclass
class JoiningTenant:
    userId: str

    @staticmethod
    async def fromRequest(request: Request):
        schema = createSchema()
        json = await request.json()
        return JoiningTenant(**schema.load(dict(**json)))
