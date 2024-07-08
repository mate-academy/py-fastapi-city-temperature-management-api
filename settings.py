from dotenv import load_dotenv
import os
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Temperature Management API"

    DATABASE_URL: str = os.environ.get("DB_URL")

    WEATHER_API: str = os.environ.get("WEATHER_API")
    WEATHER_API_KEY: str = os.environ.get("WEATHER_API_KEY")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
