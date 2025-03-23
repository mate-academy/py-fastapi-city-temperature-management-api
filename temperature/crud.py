import asyncio

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models, service
from city import models as city_models


async def get_temperature_by_city_id(db: AsyncSession, city_id: int):
    query = (
        select(models.Temperature)
        .where(models.Temperature.city_id == city_id)
        .order_by(models.Temperature.date_time.desc())
    )

    db_temperature = await db.execute(query)
    return [row[0] for row in db_temperature.fetchall()]


async def get_temperature_list(db: AsyncSession):
    query = select(models.Temperature).order_by(
        models.Temperature.city_id.asc(),
        models.Temperature.date_time.desc()
    )
    temperature_list = await db.execute(query)
    return [result[0] for result in temperature_list.fetchall()]


async def update_temperature_for_city(
    db: AsyncSession,
    city_name: str,
    city_id: int,
    client: AsyncClient
):
    temperature = await service.get_temperature_for_city(
        city_name=city_name,
        client=client
    )

    if temperature:
        new_temperature = models.Temperature(
            city_id=city_id,
            temperature=temperature
        )

        db.add(new_temperature)
        return new_temperature

    return None


async def update_all_cities_temperatures(
    db: AsyncSession,
    cities: list[city_models.City]
):
    tasks = []

    async with AsyncClient() as client:
        for city in cities:
            tasks.append(
                update_temperature_for_city(
                    db=db,
                    city_name=city.name,
                    city_id=city.id,
                    client=client
                )
            )

        results = await asyncio.gather(*tasks, return_exceptions=True)

    valid_results = []
    for result in results:
        if isinstance(result, Exception):
            continue
        if result:
            valid_results.append(result)

    await db.commit()

    await asyncio.gather(*[db.refresh(result) for result in valid_results])

    return valid_results
