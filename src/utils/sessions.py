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
from src.modules.SnapshotManaging.dtos.Snapshot import Snapshot


class SessionKeys(str, Enum):
    Credentials = r"credentials"
    Tenant = r"tenant"
    Permission = r"permission"
    Snapshot = r"snapshot"

    def __str__(self):
        return self.value


def withCredentials(request: Request):
    credentials: Optional[Credentials] = request.scope.get(
        SessionKeys.Credentials)
    return credentials


def ensureUserIsAuthenticated(request: Request):
    credentials: Optional[Credentials] = withCredentials(request)
    if credentials is None:
        raise UserUnauthenticated()
    return credentials


def withTenant(request: Request):
    tenant: Optional[Tenant] = request.scope.get(
        SessionKeys.Tenant)
    return tenant


def ensureTenantIsSpecified(request: Request):
    tenant: Optional[Tenant] = withTenant(request)
    if tenant is None:
        raise PermissionDenied()
    return tenant


def withPermission(request: Request):
    permission: Optional[Permission] = request.scope.get(
        SessionKeys.Permission)
    return permission


def ensureUserHasPermission(request: Request, mustBeApproved: bool = True, mustBeOwner: bool = False):
    permission: Optional[Permission] = withPermission(request)
    if permission is None:
        raise PermissionDenied()
    if mustBeApproved and permission.get("status") != PermissionStatuses.Approved:
        raise PermissionDenied()
    if mustBeOwner and permission.get("role") != Roles.Owner:
        raise PermissionDenied()
    return permission


def withSnapshot(request: Request):
    ownership: Optional[Snapshot] = request.scope.get(
        SessionKeys.Snapshot)
    return ownership


def ensureSnapshotIsSpecified(request: Request):
    ownership: Optional[Snapshot] = withSnapshot(request)
    if ownership is None:
        raise PermissionDenied()
    return ownership
