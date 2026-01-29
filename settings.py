from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "CITY TEMPERATURE MANAGEMENT API"
    DATABASE_URI: str = "sqlite+aiosqlite:///./db.sqlite"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
