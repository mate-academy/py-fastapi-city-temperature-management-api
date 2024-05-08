from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI city temperature"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./fast-api-city.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
