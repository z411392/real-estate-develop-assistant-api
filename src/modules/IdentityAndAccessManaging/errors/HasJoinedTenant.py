from json import dumps


class HasJoinedTenant(Exception):
    def __init__(self, userId: str, tenantId: str):
        super().__init__(
            self,
            dumps(
                dict(
                    type="HasJoinedTenant",
                    payload=dict(
                        userId=userId,
                        tenantId=tenantId,
                    ),
                )
            ),
        )
