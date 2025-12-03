from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./temperatures.db"


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(bind=engine, сlass_=AsyncSession, expire_on_commit=False, autoflush=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def get_db():
    async with SessionLocal() as db:
        yield db
