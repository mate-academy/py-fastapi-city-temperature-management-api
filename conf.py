from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./db.sqlite3"
    WEATHERAPI_KEY: str = ""
    WEATHERAPI_URL: str = f"https://api.weatherapi.com/v1"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
