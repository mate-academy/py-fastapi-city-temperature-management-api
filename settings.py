import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI city temperature management api"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./database.db"

    WEATHER_API_URL: str = "http://api.weatherapi.com/v1/current.json"

    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
