from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature.db"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
