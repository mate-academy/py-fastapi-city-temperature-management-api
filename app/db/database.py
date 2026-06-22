from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URI = "sqlite:///./city_temperature_management_api.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass