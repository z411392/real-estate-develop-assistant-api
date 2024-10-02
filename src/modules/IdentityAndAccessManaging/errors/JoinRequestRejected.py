from json import dumps


class JoinRequestRejected(Exception):
    def __init__(self, userId: str, tenantId: str):
        super().__init__(
            self,
            dumps(
                dict(
                    type="JoinRequestRejected",
                    payload=dict(
                        userId=userId,
                        tenantId=tenantId,
                    ),
                )
            ),
        )
