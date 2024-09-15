import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./city_temperature.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)
AsyncSessionLocal = sqlalchemy.orm.sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()
