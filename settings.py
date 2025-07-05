from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI City Temperature Management API"
    DATABASE_URL: Optional[str] = "sqlite+aiosqlite:///./database.db"
    WEATHER_API_URL: str
    WEATHER_API_KEY: str

    model_config = {"case_sensitive": True, "env_file": ".env"}


settings = Settings()
