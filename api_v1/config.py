from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    ECHO: bool = False

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
