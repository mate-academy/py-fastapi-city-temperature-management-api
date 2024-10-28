import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature.db"
    API_PREFIX = "/api/v1"
    WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
