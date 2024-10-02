from json import dumps


class NoModelAvailable(Exception):
    def __init__(self, tokensDifference: int):
        super().__init__(
            self,
            dumps(
                dict(
                    type="NoModelAvailable",
                    payload=dict(
                        tokensDifference=tokensDifference,
                    ),
                )
            ),
        )
