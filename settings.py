from pydantic.v1 import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "City CRUD API"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city.db"

    WEATHER_URL = "https://weatherapi-com.p.rapidapi.com/current.json"

    HEADERS = {
        "X-RapidAPI-Key": os.environ["API_KEY"],
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
