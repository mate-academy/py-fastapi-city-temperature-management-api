from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEOCODING_URL: str = "https://geocoding-api.open-meteo.com/v1/search"
    FORECAST_URL: str = "https://api.open-meteo.com/v1/forecast"
    PROJECT_NAME: str = "FastAPI city temperature management"

    DATABASE_URL: str | None = (
        "sqlite+aiosqlite:///./py-fastapi-city-temperature-management-api.db"
    )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
