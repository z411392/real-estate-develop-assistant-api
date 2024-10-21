from starlette.responses import JSONResponse
from starlette.requests import Request


async def onCheckingReadiness(request: Request):
    return JSONResponse({})
