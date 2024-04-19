import os
import httpx

from typing import List
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import schemas
from city.models import City
from temperature.models import Temperature


load_dotenv()

API_KEY = os.environ.get("API_KEY")
URL = os.environ.get("URL")


async def get_temperature_records_for_city(
        city_id: int,
        db: AsyncSession
) -> List[Temperature]:
    query = select(Temperature).filter(Temperature.city_id == city_id)
    city_temperature = await db.execute(query)

    return [temperature[0] for temperature in city_temperature.fetchall()]


async def get_all_temperature_records(db: AsyncSession) -> List[Temperature]:
    query = select(Temperature)
    temperatures = await db.execute(query)

    return [temperature[0] for temperature in temperatures.fetchall()]


async def update_temperature_record(city: City) -> Temperature:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            URL, params={"key": API_KEY, "q": city.name}
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to fetch temperature data for {city.name}"
        )

    weather = response.json()["current"]

    temperature_data = schemas.TemperatureCreate(
        city_id=city.id,
        temperature=weather["temp_c"],
        date_time=weather["last_updated"]
    )
    return Temperature(**temperature_data.model_dump())


async def update_db_record(temperature: Temperature, db: AsyncSession) -> None:
    db.add(temperature)
    await db.commit()
