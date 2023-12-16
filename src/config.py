from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

    DATABASE_URL_ENV: str | None
    WEATHER_URL: str = "https://api.weatherapi.com/v1/current.json"
    WEATHERAPI_KEY: str


settings = AppSettings()
