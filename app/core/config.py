"""Application settings using pydantic-settings.
- SRP: Only configuration responsibility.
- DIP: Other layers depend on this abstraction, not env access directly.
"""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = Field(default="DreamJournalAPI")
    env: str = Field(default="dev")
    api_v1_str: str = Field(default="/api/v1")


    secret_key: str
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60)


    sqlalchemy_database_uri: str
    media_dir: str = Field(default="./media")


    class Config:
        env_file = ".env"


settings = Settings()