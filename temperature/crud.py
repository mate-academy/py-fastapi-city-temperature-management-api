from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from city.crud import get_city_by_id
from temperature import models, schemas


async def get_all_temperatures(db: AsyncSession, city_id: int = None):
    selection = select(models.Temperature).options(
        selectinload(models.Temperature.city)
    )
    if city_id:
        city = await get_city_by_id(db, city_id)
        if city:
            selection = selection.where(models.Temperature.city_id == city.id)
    result = await db.execute(selection)
    return result.scalars().all()


async def create_temperature(
    db: AsyncSession, temperature: schemas.TemperatureCreate
) -> tuple[float, datetime]:
    city = await get_city_by_id(db, temperature.city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    created = models.Temperature(
        city_id=city.id,
        temperature=temperature.temperature,
        date_time=temperature.date_time,
    )
    db.add(created)
    await db.commit()
    await db.refresh(created)
    return created.temperature, created.date_time
