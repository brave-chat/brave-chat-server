from fastapi import (
    FastAPI,
    Request,
)
from fastapi.middleware.cors import (
    CORSMiddleware,
)
import logging
import time
import uvicorn

from app.auth import (
    router as auth_router,
)
from app.chats import (
    router as chats_router,
)
from app.config import (
    Settings,
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
from app.utils.session import (
    SQLALCHEMY_DATABASE_URL,
    database,
    init_models,
)

logger = logging.getLogger(__name__)

# change this if in production
if not Settings().DEBUG:
    chat_app = FastAPI(
        docs_url="/docs",
        redoc_url="/redocs",
        title="Realtime Chat App",
        description="Realtime Chat App Backend",
        version="1.0",
        openapi_url="/api/v1/openapi.json",
    )
else:
    chat_app = FastAPI(
        debug=True,
        title="API",
        openapi_url=None,
        docs_url=None,
        redoc_url=None,
    )

origins = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://localhost:3000",
]

chat_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@chat_app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    request.state.connection = database
    response = await call_next(request)
    start_time = time.time()
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


@chat_app.on_event("startup")
async def startup():
    await init_models(SQLALCHEMY_DATABASE_URL)
    await database.connect()


@chat_app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@chat_app.get("/api")
async def root():
    return {"message": "Welcome to this blazingly fast realtime chat app."}


chat_app.include_router(auth_router.router, tags=["Auth"])
chat_app.include_router(users_router.router, tags=["User"])
chat_app.include_router(contacts_router.router, tags=["Contact"])
chat_app.include_router(chats_router.router, tags=["Chat"])
chat_app.include_router(rooms_router.router, tags=["Room"])


def serve() -> None:
    try:
        uvicorn.run(
            "app.main:chat_app",
            host="0.0.0.0",
            workers=4,
            port=8000,
            reload=True,
            debug=True,
        )
    except Exception as e:
        print(e)


if __name__ == "__main__":
    serve()
