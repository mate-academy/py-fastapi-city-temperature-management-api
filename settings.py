from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Temperature"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./temperature_manager.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
