"""Configurations module."""

# conflict between isort and pylint
# pylint: disable=C0411
from aioredis import (
    from_url,
)
import os
from pathlib import (
    Path,
)
from pydantic import (
    BaseSettings,
)
from tempfile import (
    gettempdir,
)
from typing import (
    List,
)

TEMP_DIR = Path(gettempdir())


class Settings(BaseSettings):
    """
    A Pydantic class that loads and stores environment variables in memory.

    Note:
        The os.getenv is used in production.

    Args:
        REDIS_HOST (str) : Redis host url.
        REDIS_PORT (str) : Redis host port number.
        REDIS_USERNAME (str) : Redis host username.
        REDIS_PASSWORD (str) : Redis host password.
        SINGLESTORE_HOST (str) : SingleStore or MYSQL URL.
        SINGLESTORE_PORT (str) : SingleStore or MYSQL port number.
        SINGLESTORE_USERNAME (str) : SingleStore or a local MYSQL username.
        SINGLESTORE_PASSWORD (str) : SingleStore or a local MYSQL password.
        SINGLESTORE_DATABASE (str) : SingleStore or a local MYSQL database name.
        JWT_SECRET_KEY (str) : A secure app jwt secret key.
        DETA_PROJECT_KEY (str) : A Deta project key.
        DEBUG (bool) : A variable used to separate testing env from production env.
        CORS_ORIGINS (str) : A string that contains comma separated urls for cors origins.
        PROMETHEUS_DIR (str) : A temporary posix path for prometheus metrics.

    Example:
        >>> REDIS_HOST=redis-123456789.ec2.cloud.redislabs.com
        >>> REDIS_HOST=15065
        >>> REDIS_USERNAME=default
        >>> REDIS_PASSWORD=51R0NGPO$$W0RD
        >>> SINGLESTORE_HOST=svc-123456789.svc.singlestore.com
        >>> SINGLESTORE_PORT=3306
        >>> SINGLESTORE_USERNAME=admin
        >>> SINGLESTORE_PASSWORD=51R0NGPO$$W0RD
        >>> SINGLESTORE_DATABASE=chat
        >>> JWT_SECRET_KEY=123SDA23sa
        >>> DETA_PROJECT_KEY=12312dSDJHJSBA
        >>> DEBUG=bool("") # False, anything else True
        >>> CORS_ORIGINS="https://app-name.herokuapp.com,http://app-name.pages.dev"
        >>> PROMETHEUS_DIR="/tmp/prom"
    """

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
    DETA_PROJECT_KEY: str = os.getenv("DETA_PROJECT_KEY")
    DEBUG: str = bool(os.getenv("DEBUG"))
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS")
    PROMETHEUS_DIR: Path = TEMP_DIR / "prom"

    class Config:  # pylint: disable=R0903
        """
        A class used to set Pydantic configuration for env vars.
        """

        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def db_url(self) -> str:
        """
        Assemble database URL from self.

        Args:
            self ( _obj_ ) : object reference.

        Returns:
            str: The assembled database URL.
        """

        if bool(self.DEBUG):
            sqlalchemy_database_url = (
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
            sqlalchemy_database_url = (
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
        return sqlalchemy_database_url

    @property
    def cors_origins(self) -> List[str]:
        """
        Build a list of urls from a comma separated values string.

        Args:
            self ( _obj_ ) : object reference.

        Returns:
            List[str]: A list of urls.
        """
        return (
            [url.strip() for url in self.CORS_ORIGINS.split(",") if url]
            if self.CORS_ORIGINS
            else []
        )

    async def redis_conn(self) -> str:
        """
        Assemble Redis URL from self.

        Args:
            self ( _obj_ ) : object reference.

        Returns:
            str: The assembled Redis host URL.
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

# Export module

__all__ = ["settings"]
