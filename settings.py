from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City temperature API"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city.db"
    # DATABASE_URL: str | None = "postgresql:" \
    #                            "//user:password@postgresserver/db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
