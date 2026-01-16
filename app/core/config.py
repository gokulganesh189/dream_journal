"""Application settings using pydantic-settings.
- SRP: Only configuration responsibility.
- DIP: Other layers depend on this abstraction, not env access directly.
"""
from pydantic_settings import BaseSettings
from pydantic import Field
import os


ENV = os.environ.get("ENV", "local")


class Settings(BaseSettings):
    app_name: str = "DreamJournalAPI"
    env: str = ENV
    api_v1_str: str = "/api/v1"

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    sqlalchemy_database_uri: str
    media_dir: str = "./media"

    class Config:
        env_file = f".env.{ENV}"
        env_file_encoding = "utf-8"


settings = Settings()
