from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI city temperature management"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city.db"

    class Config:
        case_sensitive = True
        env_feli = ".env"


settings = Settings
