from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    API_V1_PREFIX: str = "/api/v1"
    OPENWEATHER_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()