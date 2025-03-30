from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


DATABASE_URL = "sqlite+aiosqlite:///src/database/source/city_temp.db"

engine = create_async_engine(DATABASE_URL, echo=True)
SQLiteSession = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with SQLiteSession() as session:
        yield session
