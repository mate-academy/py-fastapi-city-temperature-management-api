from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Temperature in Cities"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./temperature.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
