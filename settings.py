import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Weather API"
    DATABASE_URL: str | None = "sqlite:///./city_temperature_management.db"
    WEATHER_API_KEY: str = os.environ.get("WEATHER_API_KEY")

    class Config:
        case_insensitive = True
        env_file = ".env"


settings = Settings()
