from sqlalchemy.future import select

import asyncio

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import database
import models
from temperature import temp_script


async def get_all_temperatures(db: Session = Depends(database.get_db)):
    temperatures = db.execute(select(models.Temperature))
    return temperatures.scalars().all()


async def get_one_temperature_by_city_id(
        city_id: int,
        db: Session = Depends(database.get_db)
):
    temperature = db.execute(
        select(models.Temperature).filter(models.Temperature.city_id == city_id)
    ).scalars().first()

    if not temperature:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with the id {city_id} does not exist"
        )

    return temperature


async def update_all_temperatures(
       db: Session = Depends(database.get_db)
):
    cities = db.execute(select(models.City)).scalars().all()

    tasks = []

    for city in cities:
        task = asyncio.create_task(update_temperature_for_city(city, db))
        tasks.append(task)

    await asyncio.gather(*tasks)
    db.commit()
    return "Temperature data updated successfully"


async def get_temperature_data(city: models.City) -> dict:
    try:
        temperature_data = await temp_script.get_weather(city)
        return temperature_data
    except ValueError as error:
        print(f"Failed to get temperature data for city {city.name}: {str(error)}")
        return {}


async def update_temperature_for_city(city: models.City, db: Session = Depends(database.get_db)):
    temperature_data = await get_temperature_data(city)

    temperature = db.execute(
        select(models.Temperature).filter(models.Temperature.city_id == city.id)
    ).scalars().first()

    if temperature:
        temperature.date_time = temperature_data["date_time"]
        temperature.temperature = temperature_data["temperature"]
    else:
        new_temperature = models.Temperature(
            city_id=city.id,
            date_time=temperature_data["date_time"],
            temperature=temperature_data["temperature"]
        )
        db.add(new_temperature)
