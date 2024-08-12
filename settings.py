import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Weather City"
    DATABASE_URL: str | None = os.environ["DATABASE_URL"]

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
