from starlette.responses import JSONResponse
from starlette.requests import Request


async def onCheckingLiveness(request: Request):
    return JSONResponse({})
