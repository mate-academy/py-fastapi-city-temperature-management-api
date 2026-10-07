from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City-Temperature"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./proj_db.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
