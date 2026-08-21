import asyncio
import logging

from fastapi import APIRouter, HTTPException

from config import settings
from dependencies import DbDep, ClientDep
from temperature import schemas, crud as temperature_crud
from city import crud as city_crud
from temperature.client import fetch_temperature_data

API_URL = "https://api.weatherapi.com/v1/current.json"
API_KEY = settings.WEATHER_API_KEY

router = APIRouter()


@router.post("/temperatures/update/")
async def update_temperatures(db: DbDep, client: ClientDep):
    cities = await city_crud.get_cities(db=db)
    log = {
        "created": 0,
        "ignored": 0,
        "failed": 0,
    }

    tasks = [
        fetch_temperature_data(
            city=city, api_url=API_URL, api_key=API_KEY, client=client
        )
        for city in cities
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for city, extracted_data in zip(cities, results):
        if isinstance(extracted_data, Exception):
            log["failed"] += 1
            logging.warning("Failed to fetch %s: %r", city.name, extracted_data)
            continue

        valid_data = schemas.TemperatureCreate(city_id=city.id, **extracted_data)
        temperature = await temperature_crud.get_temperature_by_city_and_time(
            db=db, city_id=valid_data.city_id, date_time=valid_data.date_time
        )
        if temperature is None:
            await temperature_crud.add_temperature(db=db, data=valid_data)
            log["created"] += 1
        else:
            log["ignored"] += 1

    await db.commit()
    return log


@router.get("/temperatures/", response_model=list[schemas.TemperatureRead])
async def get_temperatures(
    db: DbDep, city_id: int | None = None, skip: int = 0, limit: int = 10
):
    if city_id is not None and await city_crud.get_city(db=db, city_id=city_id) is None:
        raise HTTPException(
            status_code=404, detail="This city does not exist in the database"
        )
    return await temperature_crud.get_temperatures(
        db=db, city_id=city_id, skip=skip, limit=limit
    )
