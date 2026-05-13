import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "City temperature measurement"
    api_key: str
    weather_api_url: str
    database_url: str

    class Config:
        env_file = Path(__file__).parent.parent / ".env"

settings = Settings()
