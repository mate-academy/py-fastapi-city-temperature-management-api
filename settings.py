import os
from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "City temperature management api"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_catalog.db"

    API_KEY: str | None = os.getenv("API_KEY")

    WEATHER_API_URL: str | None = "https://api.weatherapi.com/v1/current.json"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
