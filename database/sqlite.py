from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from database.models import Base

engine = create_async_engine(
    url="sqlite+aiosqlite:///./sqlite3",
    echo=True
)

session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False
)

async def get_session():
    async with session_maker() as session:
        yield session


@asynccontextmanager
async def get_context():
    async with session_maker() as session:
        yield session
