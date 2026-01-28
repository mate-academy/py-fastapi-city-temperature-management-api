from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///database.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
