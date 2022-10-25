from asyncio import (
    current_task,
)
from fastapi import (
    FastAPI,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import (
    sessionmaker,
)

from app.config import (
    settings,
)


async def init_engine_app(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates engine, data tables and connections to the database.

    This function creates SQLAlchemy engine instance,
    data tables, session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
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
    from app.utils.mixins import (  # noqa: WPS433
        Base,
    )

    engine = create_async_engine(
        settings.db_url,
        pool_pre_ping=True,
        pool_size=30,
        max_overflow=30,
        echo_pool=True,
        future=True,
        echo=True,
        pool_recycle=3600,
    )  # recycle every hour

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_scoped_session(
        sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession,
        ),
        scopefunc=current_task,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory
