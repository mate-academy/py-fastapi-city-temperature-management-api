from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    API_PREFIX: str = "/api/v1"

    WEATHERAPI_URL: str
    WEATHERAPI_KEY: str


settings = Settings()
