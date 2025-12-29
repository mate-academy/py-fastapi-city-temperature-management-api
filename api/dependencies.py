from dotenv import load_dotenv

from database import SessionLocal

load_dotenv()


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
