import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "City temperature management FastAPI"
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
