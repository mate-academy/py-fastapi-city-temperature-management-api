import httpx
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utils import get_or_404
from . import models, schemas
from .models import City
from .models import Temperature
from .service import get_city_weather, is_exist_city_temperature, add_temperature


async def get_all_temperatures(db: AsyncSession, limit: int, offset: int) -> list[models.Temperature]:
    query = select(models.Temperature).order_by(
        models.Temperature.date_time.desc()
    ).limit(limit).offset(offset)
    temperatures_list = await db.execute(query)
    return [temperature[0] for temperature in temperatures_list.fetchall()]


async def get_city_temperatures(
        db: AsyncSession,
        city_id: int,
        limit: int,
        offset: int
) -> list[models.Temperature]:
    query = select(models.Temperature).where(models.Temperature.city_id == city_id).order_by(
        models.Temperature.date_time.desc()
    ).limit(limit).offset(offset)
    temperatures_list = await db.execute(query)
    return [temperature[0] for temperature in temperatures_list.fetchall()]


async def update_all_temperatures(db: AsyncSession) -> dict:
    query = select(models.City)
    cities_list = await db.execute(query)

    success = {}
    fatal = {}

    for city in cities_list.fetchall():
        async with httpx.AsyncClient() as client:
            if (city_temp := await get_city_weather(client, city[0])) is None:
                fatal[city[0].name] = "no remote response"
                continue

            if await is_exist_city_temperature(db, city_temp):
                print("Exists", city[0].name, city_temp.date_time)
                fatal[city[0].name] = f"exists @ {city_temp.date_time}"
                continue

            await add_temperature(db, city_temp)

            success[city[0].name] = f"{city_temp.temperature} at {city_temp.date_time}"

    await db.commit()
    return {**success, **fatal}


async def update_single_city_temperature(city_id: int, db: AsyncSession) -> schemas.Temperature:
    stored_city = await get_or_404(db, model=City, obj_id=city_id)
    async with httpx.AsyncClient() as client:
        if (city_temp := await get_city_weather(client, stored_city, raise_exception=True)) is None:
            raise HTTPException(status_code=404, detail="Data not found")

        if await is_exist_city_temperature(db, city_temp):
            print("Exists", stored_city.name, city_temp.date_time)
            raise HTTPException(status_code=400, detail="City temperature already exists")

        result = await add_temperature(db, city_temp)

    await db.commit()

    response = schemas.Temperature(
        temperature=city_temp.temperature,
        date_time=city_temp.date_time,
        city_id=city_temp.city_id,
        id=result.lastrowid
    )
    return response
