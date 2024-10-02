from json import dumps


class UserUnauthenticated(Exception):
    def __init__(self):
        super().__init__(
            self,
            dumps(
                dict(
                    type="UserUnauthenticated",
                    payload=dict(),
                )
            ),
        )
