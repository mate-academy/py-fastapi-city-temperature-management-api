from fastapi import (
    HTTPException,
)

from sqlalchemy import (
    select,
)

from sqlalchemy.orm import selectinload

from .services import get_temperature
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from .models import Temperature

WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"


async def get_all_temperatures(db: AsyncSession) -> list[Temperature]:
    stmt = (
        select(Temperature)
        .options(selectinload(Temperature.city))
    )

    result = await db.execute(stmt)
    return result.scalars().all()


async def update_all_temperatures(db: AsyncSession) -> list[Temperature]:
    try:
        cities = await db.scalars(select(City))
        cities = list(cities.all())

        new_temperatures = []
        for city in cities:
            temperature = await get_temperature(city.name)
            db_temp = Temperature(
                temperature=temperature,
                city_id=city.id
            )
            new_temperatures.append(db_temp)

        db.add_all(new_temperatures)
        await db.commit()

        stmt = (
            select(Temperature)
            .options(selectinload(Temperature.city))
            .where(Temperature.id.in_([t.id for t in new_temperatures]))
        )

        result = await db.execute(stmt)
        return result.scalars().all()

    except Exception as error:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


async def get_city_temperatures(
    db: AsyncSession,
    city_id: int
) -> list[Temperature]:
    temperatures = await db.scalars(
        select(Temperature).where(Temperature.city_id == city_id)
    )

    return list(temperatures.all())
