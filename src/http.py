from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.exceptions import ExceptionMiddleware
from src.bootstrap import bootstrap as lifespan
from src.modules.IdentityAndAccessManaging.presentation.middlewares.withIdentityResolving import (
    withIdentityResolving,
)
from src.modules.IdentityAndAccessManaging.presentation.middlewares.withPermissionResolving import (
    withPermissionResolving,
)
from src.modules.IdentityAndAccessManaging.presentation.middlewares.withSnapshotOwnershipResolving import (
    withSnapshotOwnershipResolving,
)
from src.modules.SystemMaintaining.presentation.controllers.onCheckingLiveness import (
    onCheckingLiveness,
)
from src.modules.SystemMaintaining.presentation.controllers.onCheckingReadiness import (
    onCheckingReadiness,
)
from src.modules.SystemMaintaining.presentation.controllers.onRetrievingSystemInfo import (
    onRetrievingSystemInfo,
)
from src.modules.TenantManaging.presentation.controllers.onListingTenants import (
    onListingTenants,
)
from src.modules.TenantManaging.presentation.controllers.onCountingTenants import (
    onCountingTenants,
)
from src.modules.TenantManaging.presentation.controllers.onCreatingTenant import (
    onCreatingTenant,
)
from src.modules.TenantManaging.presentation.controllers.onRetrievingTenant import (
    onRetrievingTenant,
)
from src.modules.SnapshotManaging.presentation.controllers.onUploadingSnapshot import (
    onUploadingSnapshot,
)
from src.modules.TenantManaging.presentation.controllers.onJoiningTenant import (
    onJoiningTenant,
)
from src.modules.TenantManaging.presentation.controllers.onReviewingTenantJoining import (
    onReviewingTenantJoining,
)
from src.modules.SnapshotManaging.presentation.controllers.onParsingRegistry import (
    onParsingRegistry,
)
from src.modules.SnapshotManaging.presentation.controllers.onCountingSnapshots import (
    onCountingSnapshots,
)
from src.modules.SnapshotManaging.presentation.controllers.onListingSnapshots import (
    onListingSnapshots,
)
from src.modules.SnapshotManaging.presentation.controllers.onCountingRegistries import (
    onCountingRegistries,
)
from src.modules.SnapshotManaging.presentation.controllers.onListingRegistries import (
    onListingRegistries,
)
from src.modules.SnapshotManaging.presentation.controllers.onRetrievingRegistry import (
    onRetrievingRegistry,
)
from src.modules.TenantManaging.presentation.controllers.onRetrievingMyPermission import (
    onRetrievingMyPermission,
)
from src.modules.IdentityAndAccessManaging.presentation.controllers.onCountingUsers import (
    onCountingUsers,
)
from src.modules.IdentityAndAccessManaging.presentation.controllers.onListingUsers import (
    onListingUsers,
)
from src.modules.IdentityAndAccessManaging.presentation.controllers.onRetrievingPermission import (
    onRetrievingPermission,
)
from src.modules.OpenDataManaging.presentation.controllers.onRetrievingLands import (
    onRetrievingLands,
)
from src.modules.SystemMaintaining.presentation.middlewares.withExceptionHandling import (
    withExceptionHandling,
)


def createApp():
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            ExceptionMiddleware,
            handlers={Exception: withExceptionHandling},
            debug=False,
        ),
        Middleware(
            withIdentityResolving,
        ),
    ]

    routes = [
        Route(path="/liveness_check", endpoint=onCheckingLiveness, methods=["GET"]),
        Route(path="/readiness_check", endpoint=onCheckingReadiness, methods=["GET"]),
        Route(path="/system/info", endpoint=onRetrievingSystemInfo, methods=["GET"]),
        Route(path="/tenants", endpoint=onCountingTenants, methods=["HEAD"]),
        Route(path="/tenants", endpoint=onListingTenants, methods=["GET"]),
        Route(path="/tenants", endpoint=onCreatingTenant, methods=["POST"]),
        Mount(
            path="/tenants/{tenantId}",
            middleware=[
                Middleware(
                    withPermissionResolving,
                )
            ],
            routes=[
                Route("/", endpoint=onRetrievingTenant, methods=["GET"]),
                Route("/permissions", endpoint=onJoiningTenant, methods=["POST"]),
                Route(
                    "/permissions/me",
                    endpoint=onRetrievingMyPermission,
                    methods=["GET"],
                ),
                Route(
                    "/permissions/{permissionId}",
                    endpoint=onRetrievingPermission,
                    methods=["GET"],
                ),
                Route(
                    "/permissions/{permissionId}",
                    endpoint=onReviewingTenantJoining,
                    methods=["PUT"],
                ),
                Route("/users", endpoint=onCountingUsers, methods=["HEAD"]),
                Route("/users", endpoint=onListingUsers, methods=["GET"]),
                Route("/snapshots", endpoint=onCountingSnapshots, methods=["HEAD"]),
                Route("/snapshots", endpoint=onListingSnapshots, methods=["GET"]),
                Route("/snapshots", endpoint=onUploadingSnapshot, methods=["POST"]),
                Mount(
                    path="/snapshots/{snapshotId}",
                    middleware=[
                        Middleware(withSnapshotOwnershipResolving),
                    ],
                    routes=[
                        Route(
                            "/registries",
                            endpoint=onCountingRegistries,
                            methods=["HEAD"],
                        ),
                        Route(
                            "/registries", endpoint=onListingRegistries, methods=["GET"]
                        ),
                        Route(
                            "/registries/{registryId}",
                            endpoint=onRetrievingRegistry,
                            methods=["GET"],
                        ),
                        Route(
                            "/registries/{registryId}",
                            endpoint=onParsingRegistry,
                            methods=["PUT"],
                        ),
                    ],
                ),
                Route("/lands", endpoint=onRetrievingLands, methods=["POST"]),
            ],
        ),
    ]

    app = Starlette(
        debug=False,
        routes=routes,
        middleware=middleware,
        lifespan=lifespan,
    )
    return app
