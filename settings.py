from dataclasses import Field

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str | None = "sqlite+aiosqlite:///./test.db"
    WEATHER_API_URL: str
    API_KEY: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
