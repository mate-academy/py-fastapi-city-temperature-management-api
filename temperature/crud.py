from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from temperature.models import Temperature
from temperature.create_temp_func import create_temperature


async def get_all_temperatures(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
):
    query = select(Temperature).offset(skip).limit(limit)
    temperatures_list = await db.execute(query)
    return temperatures_list.scalars().all()


async def get_temperature_by_city_id(db: AsyncSession, city_id: int):
    query = (select(Temperature)
             .where(Temperature.city_id == city_id)
             .order_by(desc(Temperature.date_time)))
    temperature = await db.execute(query)

    if temperature is None:
        raise HTTPException(
            status_code=404,
            detail=f"The city with id {city_id} does not exist"
        )

    return temperature.scalar()


async def update_temperatures(
        db: AsyncSession,
):
    cities = await db.execute(select(City))

    for city in cities.scalars():
        city_temp = await create_temperature(city.name)
        city_datetime = datetime.utcnow()

        db.add(Temperature(
            city_id=city.id,
            date_time=city_datetime,
            temperature=city_temp)
        )

    await db.commit()
