from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME = "Temperature Management API"
    SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"

    class Config:
        case_sensitive = True


settings = Settings()
