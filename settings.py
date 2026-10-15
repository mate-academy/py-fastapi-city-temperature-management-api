from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI city temperature"

    DATABASE_URL: str = "sqlite+aiosqlite:///./cities_temperature.db"

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
