import os

from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Temperature api"

    DATABASE_URL: str | None = "sqlite:///./city_temperature.db"
    WEATHER_API_URL: str | None = "http://api.weatherapi.com/v1/current.json"
    WEATHER_API_KEY: str | None = os.getenv("WEATHER_API_KEY")
    TIME_ZONE: str | None = "Europe/Kiev"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
