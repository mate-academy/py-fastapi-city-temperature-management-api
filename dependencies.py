from typing import Annotated
from fastapi import Depends
from database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def common_parameters(
    q: str | None = None, skip: int = 0, limit: int = 10
):
    return {"q": q, "skip": skip, "limit": limit}

CommonsDep = Annotated[dict, Depends(common_parameters)]
