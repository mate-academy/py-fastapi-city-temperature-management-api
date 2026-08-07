from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLITE_FILE_NAME: str
    OPENWEATHER_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=[".env", "../.env"], env_file_encoding="utf-8", extra="ignore"
    )

    @computed_field
    def construct_db_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.SQLITE_FILE_NAME}"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
