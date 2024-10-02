from starlette.responses import JSONResponse
from starlette.requests import Request
from src.utils.session import withCredentials
from src.modules.IdentityAndAccessManaging.dtos.Credentials import Credentials
from src.modules.SystemMaintaining.application.queries.RetrieveSystemInfo import RetrieveSystemInfo
from typing import Optional


async def onRetrievingSystemInfo(request: Request):
    credential: Optional[Credentials] = withCredentials(request)
    retrieveSystemInfo = RetrieveSystemInfo()
    systemInfo = await retrieveSystemInfo(credential.exp if credential is not None else None)
    payload = dict(systemInfo=systemInfo)
    return JSONResponse(dict(payload=payload))
