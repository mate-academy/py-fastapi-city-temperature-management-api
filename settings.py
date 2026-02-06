from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature Management API"
    DATABASE_URL: str = Field(description="Database URL")
    WEATHER_API_KEY: str = Field(description="Weather API Key")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )


settings = Settings()
