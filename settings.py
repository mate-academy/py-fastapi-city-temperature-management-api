from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature Management API"

    DATABASE_URL: str = "sqlite:///./db.sqlite3"

    WEATHER_API_TIMEOUT: float = 10.0

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
