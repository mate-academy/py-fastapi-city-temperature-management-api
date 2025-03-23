from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

    PROJECT_NAME: str = "City temperature management API"
    DATABASE_URL: str = "sqlite+aiosqlite:///./city_temperature-management.db"
    WEATHER_API: str


settings = Settings()
