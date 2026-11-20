from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City temperature management"

    DATABASE_URL: str | None = (
        "sqlite+aiosqlite:///./city_temperature_management.db"
    )

    WEATHER_API_KEY: str

    URL_WEATHER: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
