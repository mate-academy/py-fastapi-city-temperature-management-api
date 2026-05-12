from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.settings import settings


SQLALCHEMY_DB_URL = settings.DATABASE_URL

engine = create_async_engine(
	SQLALCHEMY_DB_URL,
	connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
	autoflush=False,
	autocommit=False,
	bind=engine,
	class_=AsyncSession
)

Base = declarative_base()
