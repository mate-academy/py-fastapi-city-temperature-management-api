import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
