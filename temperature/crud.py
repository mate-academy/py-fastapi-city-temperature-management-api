from datetime import datetime

import httpx

import os

from dotenv import load_dotenv

from fastapi import Depends, Query

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import get_db
from temperature import models
from city_crud.models import City
from temperature.schemas import TemperatureResponse

load_dotenv()

WEATHER_API_URL = os.environ.get("WEATHER_API_URL")
API_KEY = os.environ.get("API_KEY")


async def temperature_create(
    city_id: int, date_time: datetime, temperature: float, db: AsyncSession
):
    db_temperature = models.Temperature(
        city_id=city_id, date_time=date_time, temperature=temperature
    )

    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)

    return db_temperature


async def get_temperature(city_id: int, db: AsyncSession):
    result = await db.execute(select(models.Temperature).filter_by(city_id=city_id))

    db_temperature = result.scalars().first()

    return db_temperature


async def get_temperatures(
    db: AsyncSession = Depends(get_db),
    city_id: int = Query(default=None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    stmt = select(models.Temperature)

    if city_id is not None:
        stmt = stmt.filter_by(city_id=city_id)

    stmt = stmt.offset(skip).limit(limit)

    result = await db.execute(stmt)

    db_temperatures = result.scalars().all()

    return db_temperatures


async def temperature_update_all(db: AsyncSession) -> list[TemperatureResponse]:

    result = await db.execute(select(City))
    cities = result.scalars().all()

    updated_temperatures = []

    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                response = await client.get(
                    url=WEATHER_API_URL,
                    params={"key": API_KEY, "q": city.name},
                    timeout=10.0,
                )

                response.raise_for_status()
                data = response.json()

                temperature_to_update = data.get("current").get("temp_c")
                datetime_to_update = datetime.strptime(
                    data.get("location").get("localtime"), "%Y-%m-%d %H:%M"
                )

                db_temperature = await get_temperature(city_id=city.id, db=db)

                if db_temperature:
                    db_temperature.temperature = temperature_to_update
                    db_temperature.date_time = datetime_to_update
                else:
                    print(f"{city.name} doesn't have a temperature yet.")
                    db_temperature = await temperature_create(
                        db=db,
                        city_id=city.id,
                        temperature=temperature_to_update,
                        date_time=datetime_to_update,
                    )
                    print(f"Temperature for {city.name} has been created.")

                await db.commit()
                await db.refresh(db_temperature)

                updated_temperatures.append(
                    TemperatureResponse.model_validate(db_temperature)
                )

            except httpx.RequestError as e:
                print(f"Error fetching temperature for {city.name}: {e}")
            except Exception as e:
                print(f"Error updating temperature for {city.name}: {e}")

    return updated_temperatures
