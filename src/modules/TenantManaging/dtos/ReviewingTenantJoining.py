from dataclasses import dataclass


@dataclass
class ReviewingTenantJoining:
    permissionId: str
    status: str
