from json import dumps


class TenantConflict(Exception):
    def __init__(self, name: str):
        super().__init__(
            self,
            dumps(
                dict(
                    type="TenantConflict",
                    payload=dict(name=name),
                )
            ),
        )
