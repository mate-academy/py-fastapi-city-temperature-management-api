import os

import aiohttp
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from city.models import City
from temperature import schemas, models

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = os.getenv("URL")


async def fetch_temperature(city_name: str) -> float:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{URL}key={API_KEY}&q={city_name}") as response:
                data = await response.json()
                return data["current"]["temp_c"]
    except:
        raise HTTPException(status_code=404, detail="Failed to connect to server")


async def get_temperature_for_city(db: AsyncSession):
    query = select(City)
    result = await db.execute(query)
    cities_list = result.scalars().all()
    temperatures = []
    for city in cities_list:
        temperature = await fetch_temperature(city.name)
        temperatures.append({"city_id": city.id, "temperature": temperature})
    return temperatures


async def create_temp(db: AsyncSession, temp: schemas.TemperatureCreate):
    new_temp = models.Temperature(
        city_id=temp.city_id,
        date_time=temp.date_time,
        temperature=temp.temperature,
    )
    db.add(new_temp)
    await db.commit()
    await db.refresh(new_temp)
    return new_temp


async def get_temp(db: AsyncSession):
    result = await db.execute(select(models.Temperature))
    return result.scalars().all()


async def get_single_temp(db: AsyncSession, city_id: int):
    return await db.get(models.Temperature, city_id)


def get_temperatures_by_city(db: AsyncSession, city_id: int):
    return (
        db.query(models.Temperature).filter(models.Temperature.city_id == city_id).all()
    )
