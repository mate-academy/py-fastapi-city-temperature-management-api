from pydantic import ConfigDict
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature Management"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature.db"

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()
