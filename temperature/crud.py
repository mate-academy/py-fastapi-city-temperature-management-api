from typing import Sequence

import aiohttp

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from temperature.models import Temperature
from city.models import City


async def update_temperatures(db: AsyncSession, open_weather_map_key: str) -> None:
    result = await db.execute(select(City))
    cities = result.scalars().all()
    async with aiohttp.ClientSession() as session:
        for city in cities:
            async with session.get(
                    f"https://api.openweathermap.org/data/2.5/weather"
                    f"?q={city.name}"
                    f"&appid={open_weather_map_key}"
                    f"&units=metric"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    temperature = Temperature(
                        temperature=data["main"]["temp"],
                        city_id=city.id
                    )
                    db.add(temperature)
        await db.commit()


async def get_temperatures(db: AsyncSession) -> Sequence[Temperature]:
    result = await db.execute(select(Temperature))
    return result.scalars().all()


async def get_temperature_by_city_id(db: AsyncSession, city_id: int) -> Sequence[Temperature]:
    result = await db.execute(select(Temperature).where(Temperature.city_id == city_id))
    temperatures = result.scalars().all()
    if not temperatures:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return temperatures
