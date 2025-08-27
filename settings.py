from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = "sqlite+aiosqlite:///./database.db"
    WEATHER_API_URL: Optional[str]
    WEATHER_API_KEY: Optional[str]

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
