from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from database import SessionLocal, AsyncSessionLocal


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncSession:
    db = AsyncSessionLocal()

    try:
        yield db
    finally:
        await db.close()
