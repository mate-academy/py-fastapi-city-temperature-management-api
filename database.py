from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_URL = "sqlite+aiosqlite:///./temperature.db"

engine = create_async_engine(SQL_ALCHEMY_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, class_=AsyncSession)

Base = declarative_base()
