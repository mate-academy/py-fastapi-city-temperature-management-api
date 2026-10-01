from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Weather Management API"
    DATABASE_URL: str = "sqlite:///./weather.db"
    OPEN_METEO_GEOCODING_URL: str = (
        "https://geocoding-api.open-meteo.com/v1/search"
    )
    OPEN_METEO_FORECAST_URL: str = "https://api.open-meteo.com/v1/forecast"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
