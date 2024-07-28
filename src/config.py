from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENWEATHER_API_KEY: str = "a7a7fbefc785e02a7434d574acba0433"
    SQLALCHEMY_DATABASE_URL: str = "sqlite+aiosqlite:///./city_temp.db"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
