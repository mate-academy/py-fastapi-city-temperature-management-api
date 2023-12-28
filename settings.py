from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI City Temperature management"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature_service.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()