from json import dumps
from typing import List


class MustBeInPDFFormat(Exception):
    def __init__(self, expected: List[str], acutal: str):
        super().__init__(
            self,
            dumps(
                dict(
                    type="MustBeInPDFFormat",
                    payload=dict(
                        expected=expected,
                        acutal=acutal,
                    ),
                )
            ),
        )
