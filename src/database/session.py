import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


DATABASE_URL_ASYNC = (
    f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_DB_PORT')}/{os.getenv('POSTGRES_DB')}"
)

DATABASE_URL_SYNC = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_DB_PORT')}/{os.getenv('POSTGRES_DB')}"
)

engine_async = create_async_engine(DATABASE_URL_ASYNC, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine_async, class_=AsyncSession, expire_on_commit=False
)

engine_sync = create_engine(DATABASE_URL_SYNC, echo=True)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
