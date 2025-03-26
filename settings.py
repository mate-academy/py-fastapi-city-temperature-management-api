from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    SQLITE_URL: str | None = "sqlite:///temperature.db"


settings = Settings()

