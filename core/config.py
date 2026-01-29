from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    DATABASE_URL: str
    API_PREFIX: str = "/api/v1"
    API_WEATHER_KEY: str


settings = Settings()
