from pydantic_settings import BaseSettings, SettingsConfigDict
from os import environ


class Settings(BaseSettings):
    PROJECT_NAME: str = "City temperature API"
    DATABASE_URL: str = "sqlite+aiosqlite:///./city-temperature.db"
    WEATHER_API_BASE_URL: str = "https://api.weatherapi.com/v1/current.json"
    WEATHER_API_KEY: str = environ["WEATHER_API_KEY"]

    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()


