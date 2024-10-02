from starlette.requests import Request
from starlette.responses import JSONResponse
from src.modules.SnapshotManaging.application.mutations.UploadSnapshot import (
    UploadingSnapshot,
    UploadSnapshot,
)
from src.utils.sessions import (
    ensureUserIsAuthenticated,
    ensureTenantIsSpecified,
    ensureUserHasPermission,
)
from firebase_admin.firestore_async import client
from marshmallow import Schema
from src.modules.SnapshotManaging.presentation.validators.Snapshot import (
    name,
    content,
)
from google.cloud.firestore import async_transactional
from src.infrastructure.io.PDFScanner import PDFScanner


def _createValidator():
    Validator = Schema.from_dict(dict(name=name, content=content))
    validator = Validator()
    return validator


async def _createMutation(request: Request):
    validator = _createValidator()
    mutation = UploadingSnapshot(**validator.load(dict(**await request.json())))
    return mutation


async def onUploadingSnapshot(request: Request):
    credentials = ensureUserIsAuthenticated(request)
    tenant = ensureTenantIsSpecified(request)
    ensureUserHasPermission(request)
    mutation = await _createMutation(request)
    scanner = PDFScanner()
    fullText, filePath = await scanner.scan(mutation.get("content"))
    db = client()
    payload = dict()

    @async_transactional
    async def runInTransaction(transaction):
        uploadSnapshot = UploadSnapshot(db=db, transaction=transaction)
        snapshotId = await uploadSnapshot(
            credentials.get("uid"),
            tenant.get("id"),
            mutation.get("name"),
            fullText,
            filePath,
        )
        payload.update(snapshotId=snapshotId)

    await runInTransaction(db.transaction())
    return JSONResponse(dict(payload=payload))
