from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


SQL_ALCHEMY_DATABASE_URL = "sqlite:///./city_temperature.db"


engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


Base = declarative_base()