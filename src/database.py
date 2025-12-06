from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from src.settings import settings

SQLALCHEMY_DATABASE_URL = settings.SQLITE_DATABASE_URL

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)

Base = declarative_base()

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
