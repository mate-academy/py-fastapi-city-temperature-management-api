from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import settings


# engine = create_async_engine(
#     settings.DATABASE_URL, connect_args={"check_same_thread": False}
# )

# SessionLocal = async_sessionmaker(
#     autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
# )

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(settings.DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


Base = declarative_base()
