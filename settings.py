from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI City Project"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_db.sqlite3"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()