from starlette.requests import Request
from src.utils.session import ensureUserIsAuthenticated, ensureTenantIsSpecified
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.OpenDataManaging.dtos.RetrievingLands import RetrievingLands
from src.modules.OpenDataManaging.application.queries.RetrieveLands import RetrieveLands
from dataclasses import asdict


async def onRetrievingLands(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    query = await RetrievingLands.fromRequest(request)
    db = client()
    retrieveLands = RetrieveLands(db=db)
    lands = []
    async for land in retrieveLands(credentials.uid, tenant.id, query):
        lands.append(asdict(land))
    payload = dict(lands=lands)
    return JSONResponse(dict(payload=payload))
