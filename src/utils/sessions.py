from starlette.requests import Request
from src.modules.IdentityAndAccessManaging.dtos.Credentials import Credentials
from enum import Enum
from src.modules.TenantManaging.dtos.Tenant import Tenant
from src.modules.IdentityAndAccessManaging.dtos.Permission import Permission
from typing import Optional
from src.modules.IdentityAndAccessManaging.errors.UserUnauthenticated import UserUnauthenticated
from src.modules.IdentityAndAccessManaging.errors.PermissionDenied import PermissionDenied
from src.modules.IdentityAndAccessManaging.dtos.PermissionStatuses import PermissionStatuses
from src.modules.IdentityAndAccessManaging.dtos.Roles import Roles
from src.modules.IdentityAndAccessManaging.dtos.Ownership import Ownership
from src.constants import Root


class SessionKeys(str, Enum):
    Credentials = r"credentials"
    Tenant = r"tenant"
    Permission = r"permission"
    Ownership = r"ownership"

    def __str__(self):
        return self.value


def withCredentials(request: Request):
    credentials: Optional[Credentials] = request.scope.get(
        SessionKeys.Credentials)
    return credentials


def withTenant(request: Request):
    tenant: Optional[Tenant] = request.scope.get(
        SessionKeys.Tenant)
    return tenant


def withPermission(request: Request):
    permission: Optional[Permission] = request.scope.get(
        SessionKeys.Permission)
    return permission


def withOwnership(request: Request):
    ownership: Optional[Ownership] = request.scope.get(
        SessionKeys.Ownership)
    return ownership


def ensureUserIsAuthenticated(request: Request):
    credentials: Optional[Credentials] = withCredentials(request)
    if credentials is None:
        raise UserUnauthenticated()
    return credentials


def ensureTenantIsSpecified(request: Request):
    tenant: Optional[Tenant] = withTenant(request)
    if tenant is None:
        raise PermissionDenied()
    return tenant


def ensureUserHasPermission(request: Request, mustBeApproved: bool = True, mustBeOwner: bool = False):
    permission: Optional[Permission] = withPermission(request)
    if permission is None:
        raise PermissionDenied()
    if permission.userId == Root:
        return permission
    if mustBeApproved and permission.status != PermissionStatuses.Approved:
        raise PermissionDenied()
    if mustBeOwner and permission.role != Roles.Owner:
        raise PermissionDenied()
    return permission


def ensureUserHasOwnership(request: Request):
    ownership: Optional[Ownership] = withOwnership(request)
    if ownership is None:
        raise PermissionDenied()
    return ownership
