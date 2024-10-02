from starlette.requests import Request
from starlette.responses import JSONResponse
from logging import Logger
from traceback import format_exc
from json import loads
from src.modules.RegistryManaging.errors.OutOfCredits import OutOfCredits
from src.modules.IdentityAndAccessManaging.errors.HasJoinedTenant import HasJoinedTenant
from src.modules.IdentityAndAccessManaging.errors.JoinRequestAlreadySubmitted import (
    JoinRequestAlreadySubmitted,
)
from src.modules.IdentityAndAccessManaging.errors.JoinRequestRejected import (
    JoinRequestRejected,
)
from src.modules.IdentityAndAccessManaging.errors.PermissionDenied import (
    PermissionDenied,
)
from src.modules.IdentityAndAccessManaging.errors.UserUnauthenticated import (
    UserUnauthenticated,
)

from src.modules.RegistryManaging.errors.RegistryNotFound import RegistryNotFound
from src.modules.SnapshotManaging.errors.MustBeInPDFFormat import MustBeInPDFFormat
from src.modules.TenantManaging.errors.TenantConflict import TenantConflict
from src.modules.TenantManaging.errors.TenantCreatingInProgress import (
    TenantCreatingInProgress,
)
from src.modules.TenantManaging.errors.TenantNotFound import TenantNotFound
from src.utils.development import createLogger
from marshmallow import ValidationError


class ExceptionHander:
    _logger: Logger

    def __init__(self):
        self._logger = createLogger(__name__)

    def _statusCodeFor(self, exception: Exception):
        if isinstance(exception, ValidationError):
            return 400
        if isinstance(exception, UserUnauthenticated):
            return 401
        if isinstance(exception, PermissionDenied):
            return 403
        if isinstance(exception, TenantNotFound):
            return 404
        if isinstance(exception, RegistryNotFound):
            return 404
        if isinstance(exception, OutOfCredits):
            return 402
        if isinstance(exception, MustBeInPDFFormat):
            return 415
        # if isinstance(exception, InvalidFragment):
        #     return 415
        # if isinstance(exception, NoModelAvailable):
        #     return 415
        if isinstance(exception, TenantCreatingInProgress):
            return 409
        if isinstance(exception, HasJoinedTenant):
            return 409
        if isinstance(exception, JoinRequestAlreadySubmitted):
            return 409
        if isinstance(exception, JoinRequestRejected):
            return 409
        if isinstance(exception, TenantConflict):
            return 409
        return 500

    def _errorFor(self, exception: Exception):
        if isinstance(exception, ValidationError):
            message = next(iter(exception.messages))
            return dict(
                type="ValidationError",
                payload=dict(
                    message=message,
                ),
            )
        try:
            return loads(str(exception))
        except Exception:
            error = str(exception)
            return error

    async def __call__(self, request: Request, exception: Exception):
        statusCode = self._statusCodeFor(exception)
        error = self._errorFor(exception)
        if statusCode == 500:
            self._logger.error(format_exc())
        await JSONResponse(dict(error=error), status_code=statusCode)


onExceptionRaised = ExceptionHander()
