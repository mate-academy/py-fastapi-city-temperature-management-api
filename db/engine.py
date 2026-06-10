from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from settings import settings

DATABASE_URL = settings.DATABASE_URL


async_engine = create_async_engine(
    url=DATABASE_URL,
    echo=False,
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass