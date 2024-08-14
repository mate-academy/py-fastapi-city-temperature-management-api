import os
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature Management"
    DATABASE_URL: str = "sqlite+aiosqlite:///./city_temperature.db"
    WEATHER_API: str = os.getenv("WEATHER_API")
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
