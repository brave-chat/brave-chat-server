from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import Settings
from app.utils.mixins import Base

settings = Settings()

if not settings.DEBUG:
    SQLALCHEMY_DATABASE_URL = (
        "mysql+aiomysql://"
        + settings.SINGLESTORE_USERNAME
        + ":"
        + settings.SINGLESTORE_PASSWORD
        + "@"
        + settings.SINGLESTORE_HOST
        + ":"
        + settings.SINGLESTORE_PORT
        + "/"
        + settings.SINGLESTORE_DATABASE
    )
else:
    SQLALCHEMY_DATABASE_URL = (
        "mysql+aiomysql://mahmoud:password@localhost:3306/chat"
    )

database = Database(SQLALCHEMY_DATABASE_URL)


async def init_models(database_url):
    engine = create_async_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=30,
        max_overflow=30,
        echo_pool=True,
        future=True,
        echo=True,
        pool_recycle=3600,
    )  # recycle every hour

    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
