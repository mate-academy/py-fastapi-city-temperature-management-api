from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City temperature"

    DATABASE_URL: str = "sqlite+aiosqlite:///./db.sqlite3"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()