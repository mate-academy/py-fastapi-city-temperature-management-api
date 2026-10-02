from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "City Weather API"
    app_version: str = "1.0.0"

    database_url: str = "sqlite:///./weather.db"


    geocoding_api_url: str = "https://geocoding-api.open-meteo.com/v1/search"
    forecast_api_url: str = "https://api.open-meteo.com/v1/forecast"
    weather_request_timeout_seconds: float = 10.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings():
    return Settings()
