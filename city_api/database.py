from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./city_api.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with session_maker() as session:
        yield session
