from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature.db"

    class Config:
        case_sensitive = True
        enf_file = "../../.env"


settings = Settings()
