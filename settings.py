from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI in Details"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()