from __future__ import annotations

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = (
        "FastAPI application that manages city data"
        " and their corresponding temperature data"
    )

    DATABASE_URL: str = "sqlite+aiosqlite:///./city_temperature.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
