from aioredis import (
    from_url,
)
import os
from pydantic import (
    BaseSettings,
)
from typing import (
    Any,
)


class Settings(BaseSettings):

    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: str = os.getenv("REDIS_PORT")
    REDIS_USERNAME: str = os.getenv("REDIS_USERNAME")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")
    SINGLESTORE_HOST: str = os.getenv("SINGLESTORE_HOST")
    SINGLESTORE_PORT: str = os.getenv("SINGLESTORE_PORT")
    SINGLESTORE_USERNAME: str = os.getenv("SINGLESTORE_USERNAME")
    SINGLESTORE_PASSWORD: str = os.getenv("SINGLESTORE_PASSWORD")
    SINGLESTORE_DATABASE: str = os.getenv("SINGLESTORE_DATABASE")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    DEBUG: bool = os.getenv("DEBUG")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def db_url(self) -> str:
        """
        Assemble database URL from self.

        :return: database URL.
        """
        if self.DEBUG:
            SQLALCHEMY_DATABASE_URL = (
                "mysql+aiomysql://"
                + self.SINGLESTORE_USERNAME
                + ":"
                + self.SINGLESTORE_PASSWORD
                + "@"
                + self.SINGLESTORE_HOST
                + ":"
                + self.SINGLESTORE_PORT
                + "/"
                + "test"
            )

        else:
            SQLALCHEMY_DATABASE_URL = (
                "mysql+aiomysql://"
                + self.SINGLESTORE_USERNAME
                + ":"
                + self.SINGLESTORE_PASSWORD
                + "@"
                + self.SINGLESTORE_HOST
                + ":"
                + self.SINGLESTORE_PORT
                + "/"
                + self.SINGLESTORE_DATABASE
            )
        return SQLALCHEMY_DATABASE_URL

    async def redis_conn(self) -> str:
        """
        Assemble database URL from self.

        :return: database URL.
        """
        return await from_url(
            "redis://"
            + self.REDIS_USERNAME
            + ":"
            + self.REDIS_PASSWORD
            + "@"
            + self.REDIS_HOST
            + ":"
            + self.REDIS_PORT
            + "/"
            "0",
            decode_responses=True,
        )


settings = Settings()
