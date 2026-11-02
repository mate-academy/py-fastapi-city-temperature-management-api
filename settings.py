from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

    PROJECT_NAME: str = "City Temperature Management API"
    DATABASE_URL: str = "sqlite+aiosqlite:///./proj_db.db"


settings = Settings()
