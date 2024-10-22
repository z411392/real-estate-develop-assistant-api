from starlette.requests import Request
from src.utils.session import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    ensureUserHasPermission,
)
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.SnapshotManaging.dtos.ListingSnapshots import ListingSnapshots
from src.modules.SnapshotManaging.application.queries.ListSnapshots import ListSnapshots
from src.utils.storage import getObjectURL
from src.adapters.auth.UserDao import UserDao
from dataclasses import asdict
from typing import Mapping, Optional
from src.modules.IdentityAndAccessManaging.dtos.User import User


async def onListingSnapshots(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    query = await ListingSnapshots.fromRequest(request)
    db = client()
    listSnapshots = ListSnapshots(db=db)
    snapshots = []
    usersMap: Mapping[str, Optional[User]] = {}
    async for snapshot in listSnapshots(credentials.uid, tenant.id, query):
        downloadURL = await getObjectURL(snapshot.filePath)
        usersMap[snapshot.userId] = None
        snapshots.append(dict(**asdict(snapshot), downloadURL=downloadURL))
    userDao = UserDao()
    async for user in userDao.inIds(*usersMap.keys()):
        usersMap[user.id] = asdict(user)
    payload = dict(snapshots=snapshots, usersMap=usersMap)
    return JSONResponse(dict(payload=payload))
