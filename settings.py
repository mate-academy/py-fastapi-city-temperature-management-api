from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI in Details"
    DATABASE_URL: str = "sqlite+aiosqlite:///./proj_db.db"
    OPENWEATHER_API_KEY: str | None = None  # ← додано

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
