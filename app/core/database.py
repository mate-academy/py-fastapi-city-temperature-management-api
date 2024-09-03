from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine, async_sessionmaker
)

from app.core.settings import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    connect_args=(
        {"check_same_thread": False}
    ),
)

SessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db() -> AsyncSession:
        async with SessionLocal() as session:
            yield session
