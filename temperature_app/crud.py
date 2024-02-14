from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature_app.models import Temperature


async def create_update_temperature(
        db: AsyncSession,
        data: dict,
):
    for city_id, temperature in data.items():
        query = select(Temperature).filter(
            Temperature.city_id == city_id
        )
        result = await db.execute(query)
        temp_object = result.scalar()

        if not temp_object:
            new_object = Temperature(
                city_id=city_id,
                date_time=datetime.now(),
                temperature=temperature
            )
            db.add(new_object)
        else:
            temp_object.temperature = temperature
            temp_object.date_time = datetime.now()

    await db.commit()

    return {"message": "Temperature updated successfully"}


async def get_all_temperatures(db: AsyncSession) -> List[Temperature]:
    query = select(Temperature)
    result = await db.execute(query)
    temperature_list = result.scalars()
    return temperature_list


async def get_temperatures_for_city(
        db: AsyncSession,
        city_id: int
) -> Temperature:
    query = select(Temperature).filter(Temperature.city_id == city_id)
    result = await db.execute(query)
    temperature = result.scalar()
    return temperature
