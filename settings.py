from pydantic_settings import BaseSettings

API_KEY_WEATHER = "46527bf17d37498abfc91729260307"


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI in Details"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./proj_db.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
