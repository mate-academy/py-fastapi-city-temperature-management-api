from pydantic.v1 import BaseSettings


class DB_Settings(BaseSettings):
    PROJECT_NAME: str = "City temperature management api"

    DATABASE_URL: str | None = "sqlite:///./city-temp-mng-api.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = DB_Settings()
