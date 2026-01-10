from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Weather API"
    DATABASE_URL: str | None = "sqlite+aiosqlite:///./weather_db.db"

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()
