import os

from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI city temperature management"

    DATABASE_URL: str | None = "sqlite:///./city_temperature_management.db"
    ASYNC_DATABASE_URL: str | None = (
        "sqlite+aiosqlite:///./city_temperature_management.db"
    )

    WEATHER_API_KEY: str | None = os.getenv("WEATHER_API_KEY")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
