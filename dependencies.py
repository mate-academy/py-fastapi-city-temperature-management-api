from database import SessionLocal, AsyncSessionLocal


def get_db():
    with SessionLocal() as session:
        yield session


async def get_Async_db():
    async with AsyncSessionLocal() as session:
        yield session
