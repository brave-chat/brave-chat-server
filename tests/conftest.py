import pytest

import asyncio
from asyncio.events import (
    AbstractEventLoop,
)
import datetime
from fastapi import (
    FastAPI,
)
from httpx import (
    AsyncClient,
)
import json
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
    Generator,
)

from app.auth.crud import (
    register_user,
)
from app.utils.db_utils import (
    create_database,
    drop_database,
)
from app.utils.dependencies import (
    get_db_session,
)
from app.utils.session import (
    SQLALCHEMY_DATABASE_URL,
    database,
)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Create engine and databases.

    :yield: new engine.
    """
    from app.auth.model import (  # noqa: WPS433
        AccessTokens,
    )
    from app.chats.model import (  # noqa: WPS433
        Messages,
    )
    from app.contacts.model import (  # noqa: WPS433
        Contacts,
    )
    from app.rooms.model import (  # noqa: WPS433
        RoomMembers,
        Rooms,
    )
    from app.users.model import (  # noqa: WPS433
        Users,
    )
    from app.utils.mixins import (
        Base,
    )

    await create_database()

    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()
        await drop_database()


@pytest.fixture
async def dbsession(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT,
    and the rollback to it after the test completes.

    :param _engine: current engine.
    :yields: async session.
    """
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = sessionmaker(
        connection,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    session = session_maker()
    await database.connect()

    async def create_test_user():
        class User:
            def __init__(self, *args):
                self.first_name = args[0]
                self.last_name = args[1]
                self.email = args[2]
                self.password = args[3]

        user = User("test", "user", "test@example.com", "test")
        await register_user(user)

    async def delete_user():
        query = """
            DELETE FROM
              users
            WHERE email = :email
        """
        values = {
            "email": "test@example.com",
        }
        await database.execute(query, values=values)

    try:
        await create_test_user()
        yield session
    finally:
        await delete_user()
        await session.close()
        await trans.rollback()
        await connection.close()


@pytest.fixture
def fastapi_app(
    dbsession: AsyncSession,
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

    @chat_app.get("/api")
    async def root():
        return {"message": "Welcome to this blazingly fast realtime chat app."}

    chat_app.include_router(auth_router.router, tags=["Auth"])
    chat_app.include_router(users_router.router, tags=["User"])
    chat_app.include_router(contacts_router.router, tags=["Contact"])
    chat_app.include_router(chats_router.router, tags=["Chat"])
    chat_app.include_router(rooms_router.router, tags=["Room"])

    chat_app.dependency_overrides[get_db_session] = lambda: dbsession
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


@pytest.fixture
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
