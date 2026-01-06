from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    PROJECT_NAME: str = "FastAPI City Temperature managment"

    DATABASE_URL: str = "sqlite:///./city_temp_managment.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False, extra="ignore"
    )


settings = Settings()
