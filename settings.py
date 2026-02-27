from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "City-Temperature Management API"
    DATABASE_URL: str | None = "sqlite:///./city_temp.db"
    GEOCODING_API_URL: str = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_API_URL: str = "https://api.open-meteo.com/v1/forecast"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()
