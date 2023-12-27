from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City temperature recorder"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./temperature_recorder.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
