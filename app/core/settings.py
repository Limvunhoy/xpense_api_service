# app/core/settings.py
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Environment
    ENV: str = Field(default="dev")
    JWT_SECRET_KEY: str = Field(default='123')

    # Local Postgres (dev)
    POSTGRES_USER: str = Field(default="xpense")
    POSTGRES_PASSWORD: str = Field(default="secret123")
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: str = Field(default="5432")
    POSTGRES_DB: str = Field(default="xpense")

    # Supabase (prod)
    SUPABASE_PROJECT_ID: str | None = None
    SUPABASE_PASSWORD: str | None = None
    SUPABASE_USE_POOLER: bool = Field(default=False)

    class Config:
        env_file = ".env"  # auto-loads from .env
        env_file_encoding = "utf-8"
        extra = "forbid"


settings = Settings()
