import os

from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "City and temperature API"

    DATABASE_URL: str | None = os.getenv("DATABASE_URL")

    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
