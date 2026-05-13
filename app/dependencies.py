from typing import Any, AsyncGenerator

from app.database import SessionLocal


async def get_db() -> AsyncGenerator[Any, Any]:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
