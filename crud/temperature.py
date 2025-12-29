from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services import fetch_temperature_by_city_name

import models


async def update_cities_temperature(db: AsyncSession):
    result = await db.execute(select(models.City))
    cities = result.scalars().all()

    inserted = 0
    skipped = 0

    for city in cities:
        temp = await fetch_temperature_by_city_name(city.name)
        if temp is None:
            skipped += 1
            continue

        db.add(models.Temperature(city_id=city.id, temperature=temp))
        inserted += 1

    await db.flush()

    return {
        "cities_total": len(cities),
        "inserted": inserted,
        "skipped": skipped,
    }


async def get_temperature_records(db: AsyncSession):
    result = await db.execute(
        select(models.Temperature).options(selectinload(models.Temperature.city))
    )
    return result.scalars().all()


async def get_temperature_for_city(city_id: int, db: AsyncSession):
    result = await db.execute(
        select(models.Temperature)
        .where(models.Temperature.city_id == city_id)
        .options(selectinload(models.Temperature.city))
    )
    return result.scalars().all()

