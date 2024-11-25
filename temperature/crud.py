from fastapi import HTTPException

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models, schemas


async def post_temperature(
    db: AsyncSession, temperature: schemas.TemperatureCreate
) -> None:
    query = insert(models.Temperature).values(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )
    await db.execute(query)
    await db.commit()


async def get_temperature_list(db: AsyncSession) -> list[models.Temperature]:
    query = select(models.Temperature)
    temperature_list = await db.execute(query)
    return [temperature[0] for temperature in temperature_list.fetchall()]


async def get_temperature_by_city_id(
    db: AsyncSession, city_id: int
) -> models.Temperature:
    query = select(models.Temperature).where(
        models.Temperature.city_id == city_id
    )
    result = await db.execute(query)
    result = result.scalars().all()
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Temperatures for city with id {city_id} not found"
        )
    return result
