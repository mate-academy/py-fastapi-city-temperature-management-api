import asyncio

import httpx
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from settings import settings


async def get_all_cities(db: AsyncSession) -> list[models.DBCity]:
    cities = await db.scalars(select(models.DBCity))
    return cities.all()

async def get_city_by_id(
        db: AsyncSession,
        city_id: int
) -> models.DBCity | None:
    city = await db.scalar(select(models.DBCity).where(models.DBCity.id == city_id))

    if not city:
        raise HTTPException(status_code=404, detail="City wasn't Found")
    return city

async def get_city_by_name(
        db: AsyncSession, city_name: str
) -> models.DBCity | None:
    return await db.scalar(select(models.DBCity).where(models.DBCity.name == city_name))


async def create_new_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> models.DBCity:
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city

async def update_city(
        db: AsyncSession,
        city_id: int,
        city_update: schemas.CityCreate
) -> models.DBCity:
    db_city = await get_city_by_id(db, city_id)

    db_city.name = city_update.name
    db_city.additional_info = city_update.additional_info

    await db.commit()
    await db.refresh(db_city)

    return db_city

async def delete_city(
        db: AsyncSession,
        city_id: int
):
    db_city = await get_city_by_id(db=db, city_id=city_id)

    await db.delete(db_city)
    await db.commit()

    return {"message": f"City with id {city_id} was successfully deleted"}



async def fetch_temperature_for_city(city_name: str):
    url = f"https://api.aerisapi.com/conditions/{city_name}"

    async with httpx.AsyncClient() as client:
        print(f"retrieving data for {city_name}...")
        response = await client.get(
            url,
            params={
                "client_id": settings.AERIS_CLIENT_ID,
                "client_secret": settings.AERIS_CLIENT_SECRET,
            }
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to fetch weather for {city_name}: {response.text}"
        )

    data = response.json()
    print(data)

    try:
        temperature = data['response'][0]['periods'][0]['tempC']
        return float(temperature)
    except (KeyError, IndexError):
        raise HTTPException(
            status_code=500,
            detail="Invalid response format from weather API"
        )


async def update_all_temperatures(
        db: AsyncSession
) -> list[models.DBTemperature]:
    cities = await get_all_cities(db=db)

    #
    # for city in cities:
    #
    # await db.commit()

    tasks = [fetch_temperature_for_city(city.name) for city in cities]
    temp_results = await asyncio.gather(*tasks)

    created_temperatures = []

    for city, temp_value in zip(cities, temp_results):
        db_temp = models.DBTemperature(city_id=city.id, temperature=temp_value)
        db.add(db_temp)
        created_temperatures.append(db_temp)

    await db.commit()

    for db_temp in created_temperatures:
        await db.refresh(db_temp)

    return created_temperatures


async def get_all_temperatures(
        db: AsyncSession
) -> list[models.DBTemperature]:
    query = await db.scalars(select(models.DBTemperature))
    return query.all()

async def get_temperatures_by_city(
        db: AsyncSession,
        city_id: int
) -> list[models.DBTemperature]:
    query = await db.scalars(
        select(
            models.DBTemperature
        ).where(models.DBTemperature.city_id == city_id)
    )
    return query.all()
