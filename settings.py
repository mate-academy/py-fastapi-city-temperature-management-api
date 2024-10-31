from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature Management API"

    SYNC_DATABASE_URL: str | None = "sqlite:///db.sqlite3"

    ASYNC_DATABASE_URL: str | None = "sqlite+aiosqlite:///db.sqlite3"


    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
