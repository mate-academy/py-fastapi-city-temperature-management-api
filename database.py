# database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from settings import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass
