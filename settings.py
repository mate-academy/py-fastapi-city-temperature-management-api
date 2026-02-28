# settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "GET"
    DATABASE_URL: str | None = "sqlite+aiosqlite:///./temperature_mgmt.db"

    AERIS_CLIENT_ID: str
    AERIS_CLIENT_SECRET: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()