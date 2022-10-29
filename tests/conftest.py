import pytest

from fastapi import (
    FastAPI,
)
from httpx import (
    AsyncClient,
)
import json
from sqlalchemy import (
    text,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import (
    sessionmaker,
)
from typing import (
    Any,
    AsyncGenerator,
)

from app.config import (
    settings,
)
from app.utils.db_utils import (
    create_database,
    drop_database,
)


@pytest.fixture(scope="package")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(scope="package")
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Create engine and databases.

    :yield: new engine.
    """
    from passlib.context import (
        CryptContext,
    )

    from app.auth.models import (  # noqa: WPS433
        AccessTokens,
    )
    from app.chats.models import (  # noqa: WPS433
        Messages,
    )
    from app.contacts.models import (  # noqa: WPS433
        Contacts,
    )
    from app.rooms.models import (  # noqa: WPS433
        RoomMembers,
        Rooms,
    )
    from app.users.models import (  # noqa: WPS433
        Users,
    )
    from app.utils.mixins import (
        Base,
    )

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(password):
        return pwd_context.hash(password)

    settings.DEBUG = True
    engine = create_async_engine(
        settings.db_url[:-5],
        pool_pre_ping=True,
        pool_size=30,
        max_overflow=30,
        future=True,
        pool_recycle=3600,
    )  # recycle every hour
    await create_database(engine)
    autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(
            text(
                "INSERT INTO users (first_name, last_name, email, password, user_status)"  # noqa: E501
                f" VALUES ('test', 'user', 'test@example.com','{get_password_hash('test')}', 1);",  # noqa: E501
            )
        )
        await conn.execute(
            text(
                "INSERT INTO users (first_name, last_name, email, password, user_status)"  # noqa: E501
                f" VALUES ('test1', 'user1', 'test1@example.com','{get_password_hash('test')}', 1);",  # noqa: E501
            )
        )

    try:
        yield autocommit_engine
    finally:
        await drop_database(engine)
        await engine.dispose()
        await autocommit_engine.dispose()


@pytest.fixture
async def dbsession_factory(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT,
    and the rollback to it after the test completes.

    :param _engine: current engine.
    :yields: async session.
    """

    autocommit_session_factory = sessionmaker(
        _engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    return autocommit_session_factory


@pytest.fixture
async def fastapi_app(
    dbsession_factory: AsyncSession, _engine: AsyncEngine
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """

    from app.auth import (
        router as auth_router,
    )
    from app.chats import (
        router as chats_router,
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

    chat_app = FastAPI(
        docs_url="/docs",
        redoc_url="/redocs",
        title="Realtime Chat App",
        description="Realtime Chat App Backend",
        version="1.0",
        openapi_url="/api/v1/openapi.json",
    )

    @chat_app.on_event("shutdown")
    async def shutdown():
        await chat_app.state.db_engine.dispose()

    @chat_app.get("/api")
    async def root():
        return {"message": "Welcome to this blazingly fast realtime chat app."}

    chat_app.include_router(auth_router.router, tags=["Auth"])
    chat_app.include_router(users_router.router, tags=["User"])
    chat_app.include_router(contacts_router.router, tags=["Contact"])
    chat_app.include_router(chats_router.router, tags=["Chat"])
    chat_app.include_router(rooms_router.router, tags=["Room"])

    chat_app.state.db_engine = _engine
    chat_app.state.db_transactional_session_factory = dbsession_factory
    chat_app.state.db_autocommit_session_factory = dbsession_factory
    async with _engine.connect() as conn:  # noqa: WPS440
        await conn.execute(text("USE test;"))
    return chat_app  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI, anyio_backend: Any
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as acc:
        yield acc


@pytest.fixture(scope="function")
async def token(fastapi_app: FastAPI, client: AsyncClient) -> str:
    email = "test@example.com"
    password = "test"
    response = await client.post(
        url="/api/v1/auth/login",
        data={
            "username": email,
            "password": password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    dict_response = json.loads(response.content.decode())
    return dict_response["access_token"]
