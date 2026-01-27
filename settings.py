import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    Project_Name: str = "City temperature management"

    DATABASE_URL: str | None = os.environ.get("DATABASE_URL")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
