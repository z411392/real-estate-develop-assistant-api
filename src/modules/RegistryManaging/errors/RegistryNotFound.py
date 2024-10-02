from json import dumps


class RegistryNotFound(Exception):
    def __init__(self, registryId: str):
        super().__init__(
            self,
            dumps(
                dict(
                    type="RegistryNotFound",
                    payload=dict(
                        registryId=registryId,
                    ),
                )
            ),
        )
