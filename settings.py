from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City - Temperature management API"

    DATABASE_URL: str = "sqlite+aiosqlite:///./city.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
