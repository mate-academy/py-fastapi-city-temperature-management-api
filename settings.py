from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI"

    DATABASE_URL: str | None = "sqlite:///./database.db"
    API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()