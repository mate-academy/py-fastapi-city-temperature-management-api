import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "City temperature management API"
    DATABASE_URL: str = "sqlite+aiosqlite:///./city_temperature_management.db"
    WEATHER_API_KEY: str = os.environ.get("WEATHER_API_KEY")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
