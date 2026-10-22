import random
from datetime import datetime

import httpx
from fastapi import HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import DBCity
from temperature import models, schemas
from temperature.models import DBTemperature
from services import get_current_temperature


async def get_all_temperatures(db: AsyncSession) ->  list[models.DBTemperature]:
    temperatures = await db.scalars(select(models.DBTemperature))

    return temperatures.all()

async def get_temperatures_by_city_id(db: AsyncSession, city_id: int) ->  list[models.DBTemperature]:
    temperature = await db.scalars(select(models.DBTemperature).where(models.DBTemperature.city_id == city_id))

    return temperature.all()


async def create_temperature_record(db: AsyncSession, temp_data: schemas.TemperatureCreate) -> DBTemperature:
    result = await db.execute(select(DBCity).where(DBCity.id == temp_data.city_id))
    city_exists = result.scalar_one_or_none()
    if not city_exists:
        raise HTTPException(
            status_code=404,
            detail=f"City with id {temp_data.city_id} not found"
        )

    new_temperature = DBTemperature(
        city_id=temp_data.city_id,
        date_time=temp_data.date_time,
        temperature=temp_data.temperature
    )

    try:
        db.add(new_temperature)
        await db.commit()
        await db.refresh(new_temperature)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating temperature record: {e}"
        )
    return new_temperature

async def fetch_and_store_temperatures(db: AsyncSession):

    all_cities_result = await db.execute(select(DBCity))
    cities = all_cities_result.scalars().all()

    if not cities:
        return {"message": "No cities found in the database to fetch temperatures for."}

    cities_data = [{"id": city.id, "name": city.name} for city in cities]
    fetched_data = []
    client = httpx.AsyncClient()
    for city_obj in cities_data:
        try:
            city_id = city_obj["id"]
            city_name = city_obj["name"]
            current_temp = await get_current_temperature(client, city_name)

            temp_record_data = schemas.TemperatureCreate(city_id=city_id, date_time=datetime.now(), temperature=current_temp)

            await create_temperature_record(db, temp_record_data)
            fetched_data.append(
                {"city_id": city_id, "city_name": city_name, "temperature": current_temp, "status": "success"}
            )

        except Exception as e:
            print(f"Error fetching temperature for {city_name}: {e}")

    return {"message": "Temperature data updated for cities.", "details": fetched_data}

