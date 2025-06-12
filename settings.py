from pydantic.v1 import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str = "City and temperature data management"
    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature.db"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
