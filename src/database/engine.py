from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.settings import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL_ASYNC

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    #connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)