import datetime

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from city.models import City
import httpx
from . import models
from . import schemas
from dependencies import WEATHER_API_KEY, WEATHER_API_URL


async def get_temperatures(db: AsyncSession):
    query = select(models.Temperature)
    temperatures = await db.execute(query)
    return [temperature[0] for temperature in temperatures.fetchall()]


async def get_temperature_by_city(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(models.Temperature).filter(models.Temperature.city_id == city_id)
    )
    return result.scalars().first()



async def create_temperature(db: AsyncSession, temperature: schemas.TemperatureCreate):
    query = insert(models.Temperature).values(
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**temperature.model_dump(), "id": result.lastrowid}
    return resp


async def update_temperature(db: AsyncSession):
    result = await db.execute(select(City))
    cities = result.scalars().all()

    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                response = await client.get(
                    WEATHER_API_URL,
                    params={"key": WEATHER_API_KEY, "q": city.name},
                )
                if response.status_code == 200:
                    data = response.json()
                    temperature = data["current"]["temp_c"]

                    db_temperature = models.Temperature(
                        city_id=city.id,
                        date_time=datetime.datetime.now(),
                        temperature=temperature,
                    )
                    db.add(db_temperature)
                else:
                    print(
                        f"Not possible to get data for the city"
                        f" {city.name}: {response.status_code}"
                    )


            except Exception as e:
                print(
                    f"Error during getting temperature for city {city.name}: {e}"
                )
        await db.commit()
        return {"message": "Cities Temperatures has been updated successfully"}
