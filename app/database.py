from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from databases import Database

DATABASE_URL = "sqlite+aiosqlite:///./cities.db"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

database = Database(DATABASE_URL)

async def get_db():
    async with async_session_maker() as session:
        yield session
