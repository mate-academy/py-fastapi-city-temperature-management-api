from typing import Annotated
from fastapi import Depends
from database import SessionLocal


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


async def common_dependencies(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}


CommonsDependencies = Annotated[dict, Depends(common_dependencies)]
