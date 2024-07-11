from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQlALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./city_temp.db"

engine = create_async_engine(
    SQlALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    db = AsyncSessionLocal()

    try:
        yield db
    finally:
        await db.close()
