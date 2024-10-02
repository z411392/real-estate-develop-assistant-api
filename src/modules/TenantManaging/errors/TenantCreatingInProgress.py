from json import dumps


class TenantCreatingInProgress(Exception):
    def __init__(self, userId: str):
        super().__init__(
            self,
            dumps(
                dict(
                    type="TenantCreatingInProgress",
                    payload=dict(
                        userId=userId,
                    ),
                )
            ),
        )
