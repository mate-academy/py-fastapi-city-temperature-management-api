import os

from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastApi city temperature management"
    DATABASE_URL: str = os.environ.get("DATABASE_URL")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
