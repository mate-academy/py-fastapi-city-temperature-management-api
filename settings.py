import os
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature API"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature.db"

    WEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5/weather"

    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", default="your_api_key")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
