import httpx
from fastapi import Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

import dependecies
from temperature import services
from temperature.models import CityTemperature
from cities.models import City


async def get_temperatures(db: AsyncSession) -> list:
    query = select(CityTemperature)
    temperatures = await db.execute(query)
    return [temperature[0] for temperature in temperatures.fetchall()]


async def update_city_temperature(
        db: AsyncSession = Depends(dependecies.get_db)
) -> None:
    async with httpx.AsyncClient() as client:
        cities = await db.execute(select(City))

        for city in cities.scalars():
            time_measured, current_temperature = (
                await services.get_city_weather(city.name, client)
            )

            temperature = await db.execute(select(CityTemperature).where(
                CityTemperature.city_id == city.id
            ))
            temperature = temperature.scalar()  # Fetch the scalar result once

            if temperature:
                temperature.date_time = time_measured
                temperature.temperature = current_temperature
            else:
                await db.execute(insert(CityTemperature).values(
                    city_id=city.id,
                    date_time=time_measured,
                    temperature=current_temperature
                ))

        await db.commit()
