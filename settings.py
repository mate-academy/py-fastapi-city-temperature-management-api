import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature Management API"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature.db"

    DEFAULT_LIMIT: int = 20
    DEFAULT_OFFSET: int = 0

    load_dotenv()

    URL = os.environ.get("URL", "http://api.weatherapi.com/v1/current.json")
    API_KEY = os.environ.get("API_KEY")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
