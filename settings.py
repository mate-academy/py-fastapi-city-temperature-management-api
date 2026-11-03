from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "API FOR CITY AND TEMPERATURE"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./proj_db.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
