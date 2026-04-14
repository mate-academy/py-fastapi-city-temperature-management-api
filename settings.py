from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    ASYNC_DATABASE_URL: str = "sqlite+aiosqlite:///city_temperature.db"

    model_config = {"from_attributes": True}


settings = Settings()