from sqlalchemy import (
    text,
)
from sqlalchemy.ext.asyncio import (
    create_async_engine,
)

from app.config import (
    Settings,
)
from app.utils.session import (
    SQLALCHEMY_DATABASE_URL,
)

settings = Settings()


async def create_database() -> None:
    """Create a databse."""
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL[:-5],
        pool_pre_ping=True,
        pool_size=30,
        max_overflow=30,
        echo_pool=True,
        future=True,
        echo=True,
        pool_recycle=3600,
    )

    async with engine.connect() as conn:
        database_existance = await conn.execute(
            text(
                "SELECT 1 FROM INFORMATION_SCHEMA.SCHEMATA"  # noqa: S608
                " WHERE SCHEMA_NAME='test';",
            )
        )
        database_exists = database_existance.scalar() == 1

    if database_exists:
        await drop_database()

    async with engine.connect() as conn:  # noqa: WPS440
        await conn.execute(text("CREATE DATABASE test;"))


async def drop_database() -> None:
    """Drop current database."""
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL[:-5],
        pool_pre_ping=True,
        pool_size=30,
        max_overflow=30,
        echo_pool=True,
        future=True,
        echo=True,
        pool_recycle=3600,
    )
    async with engine.connect() as conn:
        await conn.execute(text("DROP DATABASE test;"))
