from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Weather API"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./proj_db.db"

    WEATHER_API_KEY: str = os.environ.get("WEATHER_API_KEY")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
