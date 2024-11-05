from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Py-fastapi-city-temperature-management-api"

    DATABASE_URL: str = "sqlite+aiosqlite:///./db"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
