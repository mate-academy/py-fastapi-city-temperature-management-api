import asyncio
import httpx

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any

from city.crud import get_cities_list
from temperature.models import DBTemperature


async def get_weather(city_name: str, api_key: str) -> dict:
    weather_url = "https://api.weatherapi.com/v1/current.json"
    params = {"q": city_name, "key": api_key}

    async with httpx.AsyncClient() as client:
        response = await client.get(weather_url, params=params)
        weather_data = response.json()

        return weather_data


async def get_all_temperatures(
        db: AsyncSession,
        city_id: int | None = None
) -> List[DBTemperature]:
    query = select(DBTemperature)

    if city_id:
        query = query.where(DBTemperature.city_id == city_id)
    temperature_list = await db.execute(query)

    return [temperature for temperature in temperature_list.scalars()]


async def update_temperature_for_city(
        city: str,
        client: httpx.AsyncClient,
        db: AsyncSession,
        api_key: str
) -> str:
    try:
        weather_data = await get_weather(city_name=city.name, api_key=api_key)
        current_temperature = weather_data.get("current").get("temp_c")

        new_temperature = DBTemperature(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=current_temperature,
        )
        db.add(new_temperature)

        return f"Temperature for {city.name} updated"

    except Exception as error:
        return (
            f"Can not update temperature for city {city.name}: "
            f"There is no such city"
        )


async def update_temperatures(db: AsyncSession, api_key: str) -> Any:
    try:
        cities_list = await get_cities_list(db=db)

        async with httpx.AsyncClient() as client:
            tasks = [
                asyncio.create_task(
                    update_temperature_for_city(city, client, db, api_key)
                )
                for city in cities_list
            ]

            results = await asyncio.gather(*tasks)
            await db.commit()

        return results

    except SQLAlchemyError as error:
        await db.rollback()
        print(f"Database error occurred: {error}. \nUpdate is failed.")
