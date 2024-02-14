import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "CityTemperature FastAPI Proj"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temp.db"

    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
