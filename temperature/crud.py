import asyncio
import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from city.crud import get_all_cities
from temperature import models, schemas

from sqlalchemy.ext.asyncio import AsyncSession

from temperature.utils import get_temperature


async def update_temperatures(db: AsyncSession) -> dict:
    cities = await get_all_cities(db=db)

    gathering = []

    for city in cities:
        gathering.append(
            asyncio.create_task(get_temperature(city.name, city.id))
        )

    results = await asyncio.gather(*gathering)

    temperatures = [
        models.Temperature(
            date_time=datetime.datetime.now(),
            city_id=res["id"],
            temperature=res["temp"]
        )
        for res in results
    ]

    db.add_all(temperatures)

    await db.commit()

    return {"detail": "All temperatures are successfully updated"}


async def get_all_temperatures(
    db: AsyncSession,
    city_id: int | None
) -> list[schemas.Temperature]:
    query = (
        select(models.Temperature)
        .options(selectinload(models.Temperature.city))
    )
    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)

    result = await db.execute(query)
    temperatures = result.scalars().all()

    return [
        schemas.Temperature(
            id=temp.id,
            city_name=temp.city.name,
            date_time=temp.date_time,
            temperature=temp.temperature,
        )
        for temp in temperatures
    ]
