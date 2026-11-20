import asyncio
from datetime import datetime

import httpx

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from temperature import models
from temperature.weather_api import get_temperature

from city import crud
from city import models as city_models


async def get_all_temperatures(
    db: AsyncSession,
    city_id: int | None
) -> list[models.Temperature]:
    stmt = select(models.Temperature).options(
        selectinload(models.Temperature.city)
    )

    if city_id:
        stmt = stmt.where(models.Temperature.city_id == city_id)

    temperatures = await db.scalars(stmt)

    return temperatures.all()


async def create_temperature(
    client: httpx.AsyncClient,
    city: city_models.City
) -> models.Temperature | None:
    temperature = await get_temperature(client=client, city=city.name)

    if temperature is not None:
        return models.Temperature(
            date_time=datetime.now(),
            temperature=temperature,
            city_id=city.id
        )


async def update_temperatures(db: AsyncSession) -> None:
    list_cities = await crud.get_all_cities(db=db)

    async with httpx.AsyncClient(timeout=7) as client:
        tasks = [create_temperature(client, city) for city in list_cities]
        results = await asyncio.gather(*tasks)

    clean_results = [
        temperature
        for temperature in results
        if temperature is not None
    ]

    db.add_all(clean_results)
    await db.commit()
