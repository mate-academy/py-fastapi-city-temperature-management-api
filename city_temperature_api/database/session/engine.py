from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./city_temperature.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True,
)

Base = declarative_base()


async def get_db():
    async with async_session_maker() as session:
        yield session
