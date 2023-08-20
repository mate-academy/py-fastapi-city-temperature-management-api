from pydantic.v1 import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Weather API"
    DATABASE_URL: str | None = "sqlite:///./weather.db"
    WEATHER_API_KEY: str = os.environ.get("WEATHER_API_KEY")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
