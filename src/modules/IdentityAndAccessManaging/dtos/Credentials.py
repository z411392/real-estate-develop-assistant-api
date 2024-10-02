from dataclasses import dataclass
from typing import Any


@dataclass
class Credentials:
    name: str
    picture: str
    iss: str
    aud: str
    auth_time: int
    user_id: str
    sub: str
    iat: int
    exp: int
    firebase: Any
    uid: str
