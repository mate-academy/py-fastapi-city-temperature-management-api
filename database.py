from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from settings import settings

from sqlalchemy.orm.decl_api import DeclarativeBase

DATABASE_URL = settings.ASYNC_DATABASE_URL

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass
