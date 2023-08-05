import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI city temperature management service"
    DATABASE_URL: str | None = "sqlite:///./city_temperature.db"
    WEATHER_API_KEY: str = os.environ.get("API_KEY")

    class Config:
        case_sensitive = True
        env_feli = ".env"


settings = Settings()