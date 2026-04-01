from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from db.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL
)

AsyncSessionGenerator = async_sessionmaker(
    autoflush=False, autocommit= False, bind=async_engine
)

class Base(DeclarativeBase):
    pass
