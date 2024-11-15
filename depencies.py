from sqlalchemy.ext.asyncio import AsyncSession


from db.engine import SessionLocal


async def get_db() -> AsyncSession:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()
