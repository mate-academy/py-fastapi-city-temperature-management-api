from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./weather.db"
    WEATHER_API_URL: str = "https://api.open-meteo.com/v1/forecast"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
