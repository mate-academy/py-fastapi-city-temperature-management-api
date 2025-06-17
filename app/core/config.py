from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI City Temperature Management API"

    SQLALCHEMY_DATABASE_URL: str = "sqlite+aiosqlite:///./library.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()