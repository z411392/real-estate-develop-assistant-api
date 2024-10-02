from typing import Any, TypedDict


class Credentials(TypedDict):
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
