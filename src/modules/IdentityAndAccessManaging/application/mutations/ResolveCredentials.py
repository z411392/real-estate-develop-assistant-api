from firebase_admin import auth
from src.modules.IdentityAndAccessManaging.dtos.Credentials import Credentials
from typing import Optional


class ResolveCredentials:

    async def __call__(self, token: str):
        try:
            decoded: Optional[dict] = auth.verify_id_token(token)
            if decoded is None:
                return None
            return Credentials(**decoded)
        except Exception:
            return None
