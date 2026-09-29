from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "City Temperature Management API"
    DATABASE_URL: str = "sqlite+aiosqlite:///./city_temperature.db"

    GEOCODING_API_URL: str = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_API_URL: str = "https://api.open-meteo.com/v1/forecast"
    WEATHER_REQUEST_TIMEOUT: float = 10.0


settings = Settings()
