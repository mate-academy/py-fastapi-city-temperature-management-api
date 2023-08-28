from database import SessionLocal


async def get_db() -> SessionLocal:
    async with SessionLocal() as session:
        yield session
