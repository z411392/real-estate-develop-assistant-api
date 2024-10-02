from json import dumps


class TenantNotFound(Exception):
    def __init__(self, tenantId: str):
        super().__init__(
            self,
            dumps(
                dict(
                    type="TenantNotFound",
                    payload=dict(
                        tenantId=tenantId,
                    ),
                )
            ),
        )
