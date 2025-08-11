from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    WTTR_API_ENDPOINT: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
