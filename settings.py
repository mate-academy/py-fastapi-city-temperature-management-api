from typing import Optional

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI City Temperature"

    DATABASE_URL: Optional[str] = "sqlite+aiosqlite:///./city_temperature.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
