from os import getenv
from asyncio import BaseEventLoop
from uvicorn import Config, Server
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.exceptions import ExceptionMiddleware
from src.bootstrap import bootstrap as lifespan
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from traceback import format_exc
from src.utils.development import onDevelopment
from src.constants import Collections
from src.modules.IdentityAndAccessManaging.presentation.middlewares.withIdentityResolving import (
    withIdentityResolving,
)
from src.modules.IdentityAndAccessManaging.presentation.middlewares.withPermissionResolving import (
    withPermissionResolving,
)
from src.modules.IdentityAndAccessManaging.presentation.middlewares.withOwnershipResolving import (
    withOwnershipResolving,
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
from src.modules.TenantManaging.presentation.controllers.onJoiningTenant import onJoiningTenant
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


async def handleException(request: Request, exception: Exception):
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
    if isinstance(exception, TenantNotFound):
        return JSONResponse(dict(message=str(exception)), status_code=404)
    if onDevelopment():
        return PlainTextResponse(content=format_exc(), status_code=500)
    return JSONResponse(dict(message=str(exception)), status_code=500)


def createApp():
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            ExceptionMiddleware, handlers={Exception: handleException}, debug=False
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
                    "/permissions/{permissionId}",
                    endpoint=onReviewingTenantJoining,
                    methods=["PUT"],
                ),
                Route("/snapshots", endpoint=onCountingSnapshots, methods=["HEAD"]),
                Route("/snapshots", endpoint=onListingSnapshots, methods=["GET"]),
                Route("/snapshots", endpoint=onUploadingSnapshot, methods=["POST"]),
                Mount(
                    path="/snapshots/{snapshotId}",
                    middleware=[
                        Middleware(
                            withOwnershipResolving,
                            resourceType=str(Collections.Snapshots),
                        ),
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


def startHttpServer(loop: BaseEventLoop):
    app = createApp()
    config = Config(
        app=app,
        host="0.0.0.0",
        port=int(getenv("PORT")),
        loop=loop,
        server_header=False,
        date_header=False,
    )
    server = Server(config=config)
    return server.serve()
