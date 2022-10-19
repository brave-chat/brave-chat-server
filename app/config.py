from pydantic import (
    BaseSettings,
)


class Settings(BaseSettings):
    SINGLESTORE_HOST: str
    SINGLESTORE_PORT: str
    SINGLESTORE_USERNAME: str
    SINGLESTORE_PASSWORD: str
    SINGLESTORE_DATABASE: str
    JWT_SECRET_KEY: str
    DEBUG: bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
