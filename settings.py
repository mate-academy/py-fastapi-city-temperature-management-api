from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Default project"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///db.sqlite3"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
