from typing import Any, AsyncGenerator

from database import SessionLocal


async def get_db() -> AsyncGenerator[Any, Any]:
    async with SessionLocal() as db:
        yield db
