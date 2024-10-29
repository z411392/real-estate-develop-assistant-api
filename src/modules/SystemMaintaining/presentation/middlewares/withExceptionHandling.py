from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from traceback import format_exc
from src.utils.development import onDevelopment


from src.modules.IdentityAndAccessManaging.errors.UserUnauthenticated import (
    UserUnauthenticated,
)
from src.modules.IdentityAndAccessManaging.errors.PermissionDenied import (
    PermissionDenied,
)
from src.modules.TenantManaging.errors.HasJoinedTenant import HasJoinedTenant
from src.modules.TenantManaging.errors.JoinRequestRejected import JoinRequestRejected
from src.modules.TenantManaging.errors.JoinRequestAlreadySubmitted import (
    JoinRequestAlreadySubmitted,
)
from src.modules.TenantManaging.errors.TenantCreatingInProgress import (
    TenantCreatingInProgress,
)
from src.modules.TenantManaging.errors.TenantNameConflict import TenantNameConflict
from src.modules.TenantManaging.errors.TenantNotFound import TenantNotFound
from src.modules.SnapshotManaging.errors.MustBeInPDFFormat import MustBeInPDFFormat
from src.modules.SnapshotManaging.errors.OutOfCredits import OutOfCredits


async def withExceptionHandling(request: Request, exception: Exception):
    if isinstance(exception, MustBeInPDFFormat):
        return JSONResponse(dict(message=str(exception)), status_code=400)
    if isinstance(exception, HasJoinedTenant):
        return JSONResponse(dict(message=str(exception)), status_code=400)
    if isinstance(exception, JoinRequestRejected):
        return JSONResponse(dict(message=str(exception)), status_code=400)
    if isinstance(exception, JoinRequestAlreadySubmitted):
        return JSONResponse(dict(message=str(exception)), status_code=400)
    if isinstance(exception, TenantCreatingInProgress):
        return JSONResponse(dict(message=str(exception)), status_code=400)
    if isinstance(exception, TenantNameConflict):
        return JSONResponse(dict(message=str(exception)), status_code=400)
    if isinstance(exception, UserUnauthenticated):
        return JSONResponse(dict(message=str(exception)), status_code=403)
    if isinstance(exception, PermissionDenied):
        return JSONResponse(dict(message=str(exception)), status_code=403)
    if isinstance(exception, OutOfCredits):
        return JSONResponse(dict(message=str(exception)), status_code=403)
    if isinstance(exception, TenantNotFound):
        return JSONResponse(dict(message=str(exception)), status_code=404)
    if onDevelopment():
        return PlainTextResponse(content=format_exc(), status_code=500)
    return JSONResponse(dict(message=str(exception)), status_code=500)
