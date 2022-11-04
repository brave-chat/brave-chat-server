from asyncio import (
    current_task,
)
from fastapi import (
    FastAPI,
)
from sqlalchemy.ext.asyncio import (
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
    from sqlalchemy import (
        text,
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
    from app.utils.mixins import (  # noqa: WPS433
        Base,
    )

    engine = create_async_engine(
        settings.db_url,
        pool_pre_ping=True,
        pool_size=30,
        max_overflow=30,
        # echo_pool=True,
        future=True,
        # echo=True,
        pool_recycle=3600,
    )  # recycle every hour

    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        # add support for emojies
        await conn.execute(
            text("ALTER TABLE messages MODIFY content TEXT CHARSET utf8mb4;")
        )

    # Refer to https://github.com/sqlalchemy/sqlalchemy/discussions/8713 for more info.  # noqa: E501
    autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")
    autocommit_session_factory = async_scoped_session(
        sessionmaker(
            autocommit_engine,
            expire_on_commit=False,
            class_=AsyncSession,
        ),
        scopefunc=current_task,
    )
    transactional_session_factory = async_scoped_session(
        sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession,
        ),
        scopefunc=current_task,
    )
    app.state.db_engine = engine
    app.state.db_transactional_session_factory = transactional_session_factory
    app.state.db_autocommit_session_factory = autocommit_session_factory
