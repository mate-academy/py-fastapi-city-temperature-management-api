from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, models


async def get_temperature_list(db: AsyncSession):
    query = select(models.Temperature).order_by(models.Temperature.id)
    temperature_list = await db.execute(query)
    return temperature_list.scalars().all()


async def get_temperature_by_city_id(db: AsyncSession, city_id: int):
    query = select(models.Temperature).where(models.Temperature.city_id == city_id)
    temperature = await db.execute(query)
    result = temperature.scalars().all()
    if result:
        return result
    raise HTTPException(status_code=404, detail="City not found")
