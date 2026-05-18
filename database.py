from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker)
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./city_temperature.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass
