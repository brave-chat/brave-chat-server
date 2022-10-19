import os
from pydantic import (
    BaseSettings,
)


class Settings(BaseSettings):
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
