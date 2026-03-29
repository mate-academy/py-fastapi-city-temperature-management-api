import asyncio
import logging
from decimal import Decimal
from typing import Sequence

import aiohttp
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from src import models
from src.core.config import WEATHER_API_KEY


async def make_request(client: aiohttp.ClientSession, name: str) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={name}&units=metric&appid={WEATHER_API_KEY}"
    async with client.get(url) as resp:
        resp.raise_for_status()
        return await resp.json()


async def update_weather(cities: Sequence[models.City]) -> dict:
    async with aiohttp.ClientSession() as client:
        tasks = [
            asyncio.create_task(make_request(client, city.name)) for city in cities
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    data = {}

    for response in responses:
        if isinstance(response, Exception):
            logging.warning(f"Exception while fetching weather data: {response}")
            continue
        try:
            name = response.get("name")
            data[name] = response["main"]["temp"]
        except KeyError as e:
            print(f'I got a KeyError - reason key: {e} does not exist')

    return data


async def update_temperature_records(db: AsyncSession):
    last_temperature_records = []
    stmt = (
        select(models.City)
        .outerjoin(models.Temperature, models.City.id == models.Temperature.city_id)
        .options(contains_eager(models.City.temperatures))
        .order_by(models.City.id, models.Temperature.date_time.desc())
    )

    result = await db.execute(stmt)
    cities = result.scalars().unique().all()

    current_temperature_records = await update_weather(cities)

    for city in cities:
        response_city_temperature = current_temperature_records.get(city.name)
        if response_city_temperature is None:
            logging.warning(f"City {city.name} is not valid or doesn't have any temperature record")
            continue
        city_temperature_records = city.temperatures
        last_record = city_temperature_records[0] if city_temperature_records else None

        new_temperature = Decimal(str(response_city_temperature))
        old_temperature = None

        if last_record is not None:
            old_temperature = last_record.temperature

        if (
                old_temperature
                and new_temperature != old_temperature
                or last_record is None
        ):
            last_temperature_records.append(
                {"city_id": city.id, "temperature": new_temperature}
            )

    if last_temperature_records:
        res = await db.scalars(
            insert(models.Temperature).returning(models.Temperature),
            last_temperature_records,
        )
        await db.commit()
        return res.all()

    return None
