from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from database import SessionLocal


async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        yield db


async def update_db_object(
        db: AsyncSession,
        current_object: BaseModel,
        new_object: BaseModel,
):
    """ Update fields of any SQLAlchemy object """
    for field, value in new_object.dict(exclude_unset=True).items():
        setattr(current_object, field, value)

    await db.refresh(current_object)

    return current_object
