from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature Management Api"
    SYNC_DATABASE_URL: str | None = "sqlite:///./test.db"
    ASYNC_DATABASE_URL: str | None = "sqlite+aiosqlite:///./test.db"

    class Config():
        case_sensitive = True
        env_file = ".env"


settings = Settings()
