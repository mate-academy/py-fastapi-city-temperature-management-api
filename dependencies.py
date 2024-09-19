from db.database import SessionLocal


async def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
