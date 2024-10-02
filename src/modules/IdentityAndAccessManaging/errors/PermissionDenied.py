from json import dumps


class PermissionDenied(Exception):
    def __init__(self):
        super().__init__(
            self,
            dumps(
                dict(
                    type="PermissionDenied",
                    payload=dict(),
                )
            ),
        )
