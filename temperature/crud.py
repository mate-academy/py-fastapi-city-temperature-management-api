import asyncio
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import services
from temperature import models
from city import models as city_models


async def get_temperature_list(
    db: AsyncSession, skip: int = 0, limit: int = 10, city_id: str | None = None
) -> Sequence[models.Temperature]:

    stmt = (
        select(models.Temperature)
        .offset(skip)
        .limit(limit)
        .order_by(models.Temperature.date_time.desc())
    )

    if city_id:
        stmt = stmt.where(models.Temperature.city_id == city_id)
    temperatures = await db.scalars(stmt)

    return temperatures.all()


async def update_temperature_list(db: AsyncSession) -> None:
    cities_query = await db.scalars(select(city_models.City))
    cities = cities_query.all()

    temperature_data = await asyncio.gather(
        *(services.get_city_temperature(city_db) for city_db in cities)
    )

    new_temperatures = (
        models.Temperature(
            city_id=city_id, temperature=temperature, error_message=error_message
        )
        for city_id, temperature, error_message in temperature_data
    )
    for new_temperature in new_temperatures:
        db.add(new_temperature)

    await db.commit()
