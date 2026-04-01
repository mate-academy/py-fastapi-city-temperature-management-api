from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


env_path = Path(__name__).resolve().parent / '.env'
class Settings(BaseSettings):
    ROOT_PASSWORD: str
    API_KEY: str = "default_api"
    USER_DB: str
    DATABASE:str
    PASSWORD: str

    @property
    def DATABASE_URL(self):
        return f"mysql+aiomysql://{self.USER_DB}:{self.PASSWORD}@temperature-db:3306/{self.DATABASE}"

    # model_config = SettingsConfigDict(env_file=env_path)


settings = Settings()  # type: ignore
