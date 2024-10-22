from dataclasses import dataclass
from marshmallow import Schema
from marshmallow.fields import String
from starlette.requests import Request


def createSchema():
    MutationSchema = Schema.from_dict({
        "name": String(),
        "content": String(),
    })
    schema: Schema = MutationSchema()
    return schema


@dataclass
class UploadingSnapshot:
    name: str
    content: str

    @staticmethod
    async def fromRequest(request: Request):
        schema = createSchema()
        json = await request.json()
        return UploadingSnapshot(**schema.load(dict(**json)))
