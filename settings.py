from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature FastAPI"

    DATABASE_URI: str | None = "sqlite:///./db.sqlite3"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
