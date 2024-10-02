from starlette.responses import JSONResponse
from starlette.requests import Request
from src.utils.sessions import withCredentials
from src.modules.IdentityAndAccessManaging.dtos.Credentials import Credentials
from src.modules.SystemMaintaining.application.queries.RetrieveSystemInfo import RetrieveSystemInfo
from typing import Optional


async def onRetrievingSystemInfo(request: Request):
    credentials: Optional[Credentials] = withCredentials(request)
    retrieveSystemInfo = RetrieveSystemInfo()
    systemInfo = await retrieveSystemInfo(credentials.get("exp") if credentials is not None else None)
    payload = dict(systemInfo=systemInfo)
    return JSONResponse(dict(payload=payload))
