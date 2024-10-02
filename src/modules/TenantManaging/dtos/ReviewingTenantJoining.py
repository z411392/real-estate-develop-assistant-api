from dataclasses import dataclass
from marshmallow import Schema
from marshmallow.fields import String
from starlette.requests import Request
from marshmallow.validate import OneOf
from src.modules.IdentityAndAccessManaging.dtos.PermissionStatuses import PermissionStatuses


def createSchema():
    MutationSchema = Schema.from_dict({
        "permissionId": String(required=True),
        "status": String(validate=OneOf([str(PermissionStatuses.Approved), str(PermissionStatuses.Rejected)]), required=True),
    })
    schema: Schema = MutationSchema()
    return schema


@dataclass
class ReviewingTenantJoining:
    permissionId: str
    status: str

    @staticmethod
    async def fromRequest(request: Request):
        schema = createSchema()
        permissionId = request.path_params.get("permissionId")
        payload = dict(**await request.json())
        payload.update(permissionId=permissionId)
        return ReviewingTenantJoining(**schema.load(payload))
