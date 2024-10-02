from json import dumps


class JoinRequestAlreadySubmitted(Exception):
    def __init__(self, userId: str, tenantId: str):
        super().__init__(
            self,
            dumps(
                dict(
                    type="JoinRequestAlreadySubmitted",
                    payload=dict(
                        userId=userId,
                        tenantId=tenantId,
                    ),
                )
            ),
        )
