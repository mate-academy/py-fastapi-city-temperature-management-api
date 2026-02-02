from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./app.db"
    temperature_provider_base_url: str = "https://wttr.in"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
