from fastapi import (
    FastAPI,
    Request,
)
from fastapi.middleware.cors import (
    CORSMiddleware,
)
import logging
import os
from prometheus_client import (
    Counter,
)
from prometheus_fastapi_instrumentator import (
    Instrumentator,
    metrics,
)
from prometheus_fastapi_instrumentator.metrics import (
    Info,
)
import shutil
import time
from typing import (
    Callable,
)
import uvicorn

from app.auth import (
    router as auth_router,
)
from app.chats import (
    router as chats_router,
)
from app.config import (
    settings,
)
from app.contacts import (
    router as contacts_router,
)
from app.rooms import (
    router as rooms_router,
)
from app.users import (
    router as users_router,
)
from app.utils.engine import (
    init_engine_app,
)
from app.web_sockets import (
    router as web_sockets_router,
)


def http_requested_languages_total() -> Callable[[Info], None]:
    METRIC = Counter(
        "http_requested_languages_total",
        "Number of times a certain language has been requested.",
        labelnames=("langs",),
    )

    def instrumentation(info: Info) -> None:
        langs = set()
        lang_str = info.request.headers["Accept-Language"]
        for element in lang_str.split(","):
            element = element.split(";")[0].strip().lower()
            langs.add(element)
        for language in langs:
            METRIC.labels(language).inc()

    return instrumentation


def setup_prometheus(app: FastAPI) -> None:  # pragma: no cover
    """
    Enables prometheus integration.

    :param app: current application.
    """
    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=True,
        # should_respect_env_var=True,
        should_instrument_requests_inprogress=True,
        # excluded_handlers=[".*admin.*", "/metrics"],
        # env_var_name="ENABLE_METRICS",
        inprogress_name="inprogress",
        inprogress_labels=True,
    )
    instrumentator.instrument(app).expose(
        app,
        should_gzip=True,
        name="prometheus_metrics",
        include_in_schema=False,
    )
    instrumentator.add(http_requested_languages_total())
    instrumentator.add(
        metrics.request_size(
            should_include_handler=True,
            should_include_method=False,
            should_include_status=True,
            metric_namespace="a",
            metric_subsystem="b",
        )
    ).add(
        metrics.response_size(
            should_include_handler=True,
            should_include_method=False,
            should_include_status=True,
            metric_namespace="namespace",
            metric_subsystem="subsystem",
        )
    )


def set_multiproc_dir() -> None:
    """
    Sets mutiproc_dir env variable.

    This function cleans up the multiprocess directory
    and recreates it. This actions are required by prometheus-client
    to share metrics between processes.

    After cleanup, it sets two variables.
    Uppercase and lowercase because different
    versions of the prometheus-client library
    depend on different environment variables,
    so I've decided to export all needed variables,
    to avoid undefined behaviour.
    """
    shutil.rmtree(settings.PROMETHEUS_DIR, ignore_errors=True)
    os.makedirs(settings.PROMETHEUS_DIR, exist_ok=True)
    os.environ["prometheus_multiproc_dir"] = str(
        settings.PROMETHEUS_DIR.expanduser().absolute(),
    )
    os.environ["PROMETHEUS_MULTIPROC_DIR"] = str(
        settings.PROMETHEUS_DIR.expanduser().absolute(),
    )


logger = logging.getLogger(__name__)

if settings.DEBUG == "info":
    chat_app = FastAPI(
        docs_url="/docs",
        redoc_url="/redocs",
        title="Brave Chat Server",
        description="The server side of Brave Chat.",
        version="1.0",
        openapi_url="/api/v1/openapi.json",
    )
else:
    chat_app = FastAPI(
        docs_url=None,
        redoc_url=None,
        title=None,
        description=None,
        version=None,
        openapi_url=None,
    )

origins = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://localhost:3000",
]

origins.extend(settings.cors_origins)

chat_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@chat_app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@chat_app.on_event("startup")
async def startup():
    await init_engine_app(chat_app)
    setup_prometheus(chat_app)


@chat_app.on_event("shutdown")
async def shutdown():
    await chat_app.state.db_engine.dispose()


@chat_app.get("/api")
async def root():
    return {"message": "Welcome to the Brave Chat Server."}


chat_app.include_router(auth_router.router, tags=["Auth"])
chat_app.include_router(users_router.router, tags=["User"])
chat_app.include_router(contacts_router.router, tags=["Contact"])
chat_app.include_router(chats_router.router, tags=["Chat"])
chat_app.include_router(rooms_router.router, tags=["Room"])
chat_app.include_router(web_sockets_router.router, tags=["Socket"])


def serve() -> None:
    try:
        set_multiproc_dir()
        uvicorn.run(
            "app:chat_app",
            host="0.0.0.0",
            workers=4,
            port=8000,
            reload=True,
            debug=True,
            log_level="debug",
        )
    except Exception as e:
        print(e)


if __name__ == "__main__":
    serve()
