import asyncio
from datetime import datetime

import httpx
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from city import models as city_models
from temperature import models


async def get_all_temperatures(db: AsyncSession, city_id: int | None = None):
    query = select(models.DBTemperature)

    if city_id is not None:
        query = query.where(models.DBTemperature.city_id == city_id)

    temperature_list = await db.execute(query)

    return [temperature for temperature in temperature_list.scalars()]


async def get_weather(city_name: str, api_key: str) -> dict:
    base_url = "https://api.weatherapi.com/v1/current.json"
    params = {"q": city_name, "key": api_key}

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
        data = response.json()
        return data


async def update_temperature_for_city(city, client, db, api_key):
    try:
        weather_data = await get_weather(city_name=city.name, api_key=api_key)
        current_temperature = weather_data["current"]["temp_c"]

        temperature_instance = models.DBTemperature(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=current_temperature,
        )

        db.add(temperature_instance)
        return f"Temperature for {city.name} updated"
    except Exception as error:
        return (
            f"Error updating temperature for city {city.name}: "
            f"city is not exist"
        )


async def update_temperature(db: AsyncSession, api_key: str):
    try:
        query = select(city_models.DBCity)
        cities_list = await db.execute(query)
        cities = cities_list.scalars()

        async with httpx.AsyncClient() as client:
            tasks = []
            for city in cities:
                tasks.append(
                    asyncio.create_task(
                        update_temperature_for_city(city, client, db, api_key)
                    )
                )
            results = await asyncio.gather(*tasks)
            await db.commit()

        return results

    except SQLAlchemyError as error:
        await db.rollback()
        print(f"Database error: {error}")
