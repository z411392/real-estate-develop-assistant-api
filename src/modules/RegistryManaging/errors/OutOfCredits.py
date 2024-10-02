from json import dumps


class OutOfCredits(Exception):
    def __init__(self, remaining: int, toBeDecucted: int):
        super().__init__(
            self,
            dumps(
                dict(
                    type="OutOfCredits",
                    payload=dict(
                        remaining=remaining,
                        toBeDecucted=toBeDecucted,
                    ),
                )
            ),
        )
