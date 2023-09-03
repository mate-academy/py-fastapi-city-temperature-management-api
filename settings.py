import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI in Details"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature_management.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

API_KEY = os.environ.get("API_KEY")
URL = os.environ.get("URL")
