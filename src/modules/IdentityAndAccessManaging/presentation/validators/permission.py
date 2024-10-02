from marshmallow.fields import String
from marshmallow.validate import OneOf
from src.modules.IdentityAndAccessManaging.dtos.PermissionStatuses import (
    PermissionStatuses,
)

permissionId = String(required=True)
status = String(
    validate=OneOf(
        [str(PermissionStatuses.Approved), str(PermissionStatuses.Rejected)]
    ),
    required=True,
)
