from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import temperature.models
import temperature.schemas


async def get_all_temperatures(db: AsyncSession):
    query = select(temperature.models.Temperature).options(selectinload(temperature.models.Temperature.city))
    result = await db.execute(query)
    temperatures = result.scalars().all()
    return temperatures


async def get_temperatures_for_city(
        db: AsyncSession,
        city_id: int
) -> list[temperature.schemas.Temperature]:
    query = (select(temperature.models.Temperature).
             options(selectinload(temperature.models.Temperature.city)).
             filter(temperature.models.Temperature.city_id == city_id))
    result = await db.execute(query)
    db_temperatures = result.scalars().all()
    temperatures = [temperature.schemas.Temperature.model_validate(db_temp)
                    for db_temp in db_temperatures]
    return temperatures


async def create_temperature(db: AsyncSession, temperatures_data: temperature.schemas.TemperatureCreate):
    db_temp = temperature.models.Temperature(**temperatures_data.model_dump())
    db.add(db_temp)
    await db.commit()
    await db.refresh(db_temp)
    return db_temp
