import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI city temperature management API"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature_management.db"

    WEATHER_API_KEY: str | None = os.getenv("WEATHER_API_KEY")

    CURRENT_WEATHER_URL: str | None = "http://api.weatherapi.com/v1/current.json"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
