from typing import Dict

from fastapi import Query
from sqlalchemy.orm import Session

from src.db.database import AsyncSessionLocal


async def get_db() -> Session:
    db = AsyncSessionLocal()

    try:
        yield db
    finally:
        await db.close()


def pagination_params(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1)
) -> Dict[str, int]:
    return {"skip": skip, "limit": limit}
