from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City-Temperature Management"
    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city-temperature.db"
    WEATHER_API_KEY = "your_weather_api_key"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
