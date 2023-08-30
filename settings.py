from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City and Temperature"

    DATABASE_URL: str = "sqlite+aiosqlite:///./city_temp.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
print(settings.DATABASE_URL)