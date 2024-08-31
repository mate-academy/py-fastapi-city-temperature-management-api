from fastapi import HTTPException
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Type


async def get_or_404(db: AsyncSession, model: Type[BaseModel], obj_id: int) -> Type[BaseModel]:
    obj = await db.get(model, obj_id)
    if obj is None:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return obj
