from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City weather api"
    SQLALCHEMY_DATABASE_URL: str = "sqlite+aiosqlite:///db.sqlite3"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
    )


settings = Settings()
