from starlette.requests import Request
from src.utils.sessions import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    ensureUserHasPermission,
)
from starlette.responses import JSONResponse
from firebase_admin.firestore_async import client
from src.modules.SnapshotManaging.application.queries.ListSnapshots import (
    ListingSnapshots,
    ListSnapshots,
)
from src.utils.storage import getObjectURL
from src.adapters.auth.UserDao import UserDao
from typing import Mapping, Optional
from src.modules.IdentityAndAccessManaging.dtos.User import User
from marshmallow import Schema
from src.utils.validators import page


def _createValidator():
    Validator = Schema.from_dict(dict(page=page))
    validator = Validator()
    return validator


async def _createQuery(request: Request):
    validator = _createValidator()
    query = ListingSnapshots(**validator.load(dict(**request.query_params)))
    return query


async def onListingSnapshots(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    query = await _createQuery(request)
    db = client()
    listSnapshots = ListSnapshots(db=db)
    snapshots = []
    usersMap: Mapping[str, Optional[User]] = {}
    async for snapshot in listSnapshots(
        credentials.get("uid"), tenant.get("id"), query
    ):
        downloadURL = await getObjectURL(snapshot.get("filePath"))
        usersMap[snapshot.get("userId")] = None
        snapshots.append(dict(**snapshot, downloadURL=downloadURL))
    userDao = UserDao()
    async for user in userDao.inIds(*usersMap.keys()):
        usersMap[user.get("id")] = user
    payload = dict(snapshots=snapshots, usersMap=usersMap)
    return JSONResponse(dict(payload=payload))
