import os
import dotenv
from pydantic.v1 import BaseSettings

dotenv.load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature"
    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_tempr.db"

    # URL to weather API to get data about weather
    CURRENT_WEATHER_URL: str = os.getenv("CURRENT_WEATHER_URL")
    # API key to be able to request to CURRENT_WEATHER_URL
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY")

    class Config:
        case_sensitive = True
        env_file = "../.env"


settings = Settings()
