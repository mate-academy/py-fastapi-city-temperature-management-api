from typing import Type

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


async def get_object_or_404(
        db: AsyncSession,
        model: Type[BaseModel],
        obj_id: int
) -> Type[BaseModel]:
    obj = await db.get(model, obj_id)

    if not obj:
        raise HTTPException(
            status_code=404,
            detail=f"{model.__name__} not found"
        )
    return obj
