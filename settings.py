from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI in Details"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature.db"

    class Config:
        case_sensitive = True


settings = Settings()
