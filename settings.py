import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Weather API"
    DATABASE_URL: str | None = "sqlite:///./weather.db"
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY")

    class Config:
        case_insensitive = True
        env_file = ".env"


settings = Settings()
