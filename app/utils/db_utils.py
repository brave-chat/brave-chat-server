from sqlalchemy import (
    text,
)


async def create_database(engine) -> None:
    """Create a databse."""

    async with engine.connect() as conn:
        database_existance = await conn.execute(
            text(
                "SELECT 1 FROM INFORMATION_SCHEMA.SCHEMATA"  # noqa: S608
                " WHERE SCHEMA_NAME='test';",
            )
        )
        database_exists = database_existance.scalar() == 1

    if database_exists:
        await drop_database(engine)

    async with engine.connect() as conn:  # noqa: WPS440
        await conn.execute(text("CREATE DATABASE test;"))
        await conn.execute(text("USE test;"))


async def drop_database(engine) -> None:
    """Drop current database."""
    async with engine.connect() as conn:
        await conn.execute(text("DROP DATABASE test;"))
