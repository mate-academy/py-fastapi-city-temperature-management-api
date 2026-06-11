from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        yield db