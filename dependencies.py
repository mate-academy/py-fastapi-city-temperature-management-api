import asyncio
from datetime import datetime
from typing import Annotated

import httpx
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from database import AsyncSessionLocal
from settings import WEATHER_REQUEST_URL, WEATHER_API_KEY
from temperature.models import Temperature


async def async_get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def async_fetch_weather_for_cities(
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> list[tuple[int, asyncio.Task]]:
    cities = await db.scalars(select(City))

    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as group:
            tasks = [
                (city.id, group.create_task(
                    client.get(
                        WEATHER_REQUEST_URL,
                        params={"key": WEATHER_API_KEY, "q": city.name}
                    )
                ))
                for city in cities.all()
            ]

    return tasks


async def async_parse_weather_responses(
    responses: Annotated[
        list[tuple[int, asyncio.Task]], Depends(async_fetch_weather_for_cities)
    ]
) -> list[Temperature]:
    temperatures = []

    for city_id, task in responses:
        result = task.result().json()
        current_data = result.get("current")
        temperatures.append(
            Temperature(
                date_time=datetime.strptime(
                    current_data.get("last_updated"), "%Y-%m-%d %H:%M"
                ),
                temperature=current_data.get("temp_c"),
                city_id=city_id,
            )
        )

    return temperatures
