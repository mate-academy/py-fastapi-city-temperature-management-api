from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from settings import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)

AsyncSession = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass
