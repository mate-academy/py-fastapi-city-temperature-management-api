from typing import List, Any, Dict

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from temperature_app import models, schemas


async def create_temperature(
        db: AsyncSession,
        temperature: schemas.TemperatureCreate
) -> Dict[str, Any]:
    query = insert(models.Temperature).values(**temperature.dict())
    result = await db.execute(query)
    await db.commit()
    response = {"id": result.lastrowid, **temperature.model_dump()}
    return response


async def get_all_temperatures(db: AsyncSession) -> List[models.Temperature]:
    query = select(models.Temperature)
    temperature_list = await db.execute(query)
    return [temp[0] for temp in temperature_list.fetchall()]


async def get_temperatures_for_city(
        db: AsyncSession,
        city_id: int
) -> List[models.Temperature]:
    query = select(models.Temperature, models.Temperature.city_id).where(models.Temperature.city_id == city_id)
    result = await db.execute(query)
    return [temp[0] for temp in result.fetchall()]
