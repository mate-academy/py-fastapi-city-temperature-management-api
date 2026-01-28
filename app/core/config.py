from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    OPEN_METEO_TIMEOUT_SECONDS: int = 10


settings = Settings()
