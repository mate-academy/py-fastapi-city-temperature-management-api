from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "City temperature management API"
    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature.db"
    WEATHER_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
