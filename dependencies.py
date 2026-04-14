from database import AsyncSessionLocal


async def get_db():
    db = AsyncSessionLocal()

    try:
        yield db
    finally:
        await db.close()