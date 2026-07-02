from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app.config import settings
from app.db.models.base import BaseModel


sync_engine = create_engine(f"sqlite:///./{settings.DATABASE_NAME}")
sync_session = sessionmaker(bind=sync_engine)


def init_db():
    BaseModel.metadata.create_all(sync_engine)


def get_db():
    db = sync_session()
    try:
        yield db
    finally:
        db.close()


async_engine = create_async_engine(
    f"sqlite+aiosqlite:///./{settings.DATABASE_NAME}",
    future=True,
    echo=True
)
async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_async_db():
    async with async_session() as db:
        yield db
