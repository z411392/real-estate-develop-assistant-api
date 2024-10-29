from starlette.requests import Request
from src.utils.sessions import ensureUserIsAuthenticated
from firebase_admin.firestore_async import client
from src.modules.TenantManaging.application.queries.CountTenants import CountTenants
from starlette.responses import Response


async def onCountingTenants(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    db = client()
    countTenants = CountTenants(db=db)
    count = await countTenants(credentials.uid)
    response = Response()
    response.headers["content-length"] = str(count)
    return response
