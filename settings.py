from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI City Temperature Management"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature_db.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
