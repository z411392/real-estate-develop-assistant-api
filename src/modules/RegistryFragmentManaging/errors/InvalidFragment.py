from json import dumps


class InvalidFragment(Exception):
    def __init__(self, snapshotId: str, registryId: str, fragmentId: str):
        super().__init__(
            self,
            dumps(
                dict(
                    type="InvalidFragment",
                    payload=dict(
                        snapshotId=snapshotId,
                        registryId=registryId,
                        fragmentId=fragmentId,
                    ),
                )
            ),
        )
