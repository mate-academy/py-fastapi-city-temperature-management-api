from pydantic.v1 import BaseSettings


class Setting(BaseSettings):
    PROJECT_NAME: str = "FastAPI City Temperature Management API"

    DATABASE_URL: str | None = \
        "sqlite+aiosqlite:///./city_temperature_management.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Setting()
