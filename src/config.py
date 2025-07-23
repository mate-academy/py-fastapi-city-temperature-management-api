from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./weather.db"

    # Weather API
    BASE_URL: str = "http://api.weatherapi.com/v1"
    WEATHER_API: str = "29a7b035c1fc4acba45172326252207"  # TRIAL Ends on 05/Aug/2025

    PROJECT_NAME: str = "Weather in the city"
    APP_VERSION: str = "1.0"

    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        env_file=('.env', '.env.prod')
    )


settings = Config()
