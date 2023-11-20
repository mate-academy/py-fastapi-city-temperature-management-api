from datetime import datetime
from typing import Any, Sequence

from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from temperature.models import Temperature


async def get_all_temperatures(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
) -> Sequence[Temperature | Any]:
    query = select(Temperature).offset(skip).limit(limit)
    temperatures_list = await db.execute(query)
    return temperatures_list.scalars().all()


async def get_temperature_by_city_id(db: AsyncSession, city_id: int) -> Temperature | Any:
    query = select(Temperature).where(Temperature.city_id == city_id)
    response = await db.execute(query)
    temperature = response.scalars().first()

    if temperature is None:
        raise HTTPException(
            status_code=404,
            detail=f"The city with id {city_id} does not exist"
        )

    return temperature


async def create_temperature_by_city(
        db: AsyncSession,
        city_id: int,
        date_time: datetime,
        temperature: float
):
    query = insert(Temperature).values(
        city_id=city_id,
        date_time=date_time,
        temperature=temperature
    )
    result = await db.execute(query)
    await db.commit()
    await db.refresh(result)

    return result
