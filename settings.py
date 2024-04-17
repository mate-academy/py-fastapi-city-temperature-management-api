from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "temperature-management-api"

    DATABASE_URL: str = "sqlite+aiosqlite:///./temperature-management-api.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
