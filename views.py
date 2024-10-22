from datetime import datetime

import requests
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from database import models


async def get_cities(db: AsyncSession):
    query = await db.execute(
        select(models.DBCity)
    )
    return query.scalars().all()


async def post_city(city: schemas.CityCreate, db: AsyncSession):
    new_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city


async def delete_city(city_id: int, db: AsyncSession):
    query = await db.execute(
        select(models.DBCity)
        .filter(models.DBCity.id == city_id)
    )

    found_city = query.scalars().first()

    if found_city:
        await db.delete(found_city)
        await db.commit()
        return True
    return False


async def fetch_data_temperature(db: AsyncSession):
    query = await db.execute(
        select(models.DBCity)
    )
    all_cities = query.scalars().all()

    async with httpx.AsyncClient() as client:
        for city in all_cities:
            url = f"http://api.weatherapi.com/v1/current.json?key=caef70c7d43a4a988c5163801242210&q={city.name}"
            response = await client.get(url)
            weather_data = response.json()
            new_temperature = models.DBTemperature(
                city_id=city.id,
                date_time=datetime.strptime(weather_data["current"]["last_updated"], "%Y-%m-%d %H:%M"),
                temperature=weather_data["current"]["temp_c"],
            )

            db.add(new_temperature)
        await db.commit()

    query_all_temperatures = await db.execute(
        select(models.DBTemperature)
    )
    result = query_all_temperatures.scalars().all()
    return result


async def get_temperatures(city_id: int, db: AsyncSession):
    if city_id:
        query = await db.execute(
            select(models.DBTemperature)
            .filter(models.DBTemperature.city_id == city_id)
        )
    else:
        query = await db.execute(
            select(models.DBTemperature)
        )
    all_temperatures = query.scalars().all()
    return all_temperatures


async def get_temperatures_of_city(city_id: int, db: AsyncSession):
    query = await db.execute(
        select(models.DBTemperature)
        .filter(models.DBTemperature.city_id == city_id)
    )
    all_temperatures = query.scalars().all()
    return all_temperatures
