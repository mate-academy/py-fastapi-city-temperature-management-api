from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)

from core import settings

engine = create_async_engine(
    url=settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = async_sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    bind=engine
)


async def get_db():
    async with SessionLocal() as db:
        yield db
