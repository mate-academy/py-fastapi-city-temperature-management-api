import asyncio
import os
from datetime import datetime
from typing import Optional

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Query
from httpx import HTTPError
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import read_cities
from city.schemas import City
from database import SessionLocal
from dependencies import get_db_session
from temperature import schemas, crud

load_dotenv()

router = APIRouter()

WEATHER_KEY = os.environ["WEATHER_KEY"]
URL = "https://api.weatherapi.com/v1/current.json"
WEATHER_URL = f"{URL}?key={WEATHER_KEY}"


@router.post(
    "/temperatures/update", response_model=list[schemas.Temperature]
)
async def update_temperatures() -> list[schemas.Temperature]:
    async with SessionLocal() as db_main:
        cities = await read_cities(db_main)

    temperature_records = []

    client = httpx.AsyncClient()

    async def fetch_temperature(city: City):
        try:
            response = await client.get(f"{WEATHER_URL}&q={city.name}")
            data = response.json()

            temp_record = schemas.TemperatureCreate(
                city_id=city.id,
                date_time=datetime.utcnow(),
                temperature=data['current']['temp_c']
            )
            async with SessionLocal() as db:
                db_record = await crud.create_temperature_record(
                    db=db, temperature_data=temp_record
                )

            temperature_records.append(db_record)

        except HTTPError as http_err:
            print(http_err)
        except Exception as err:
            print(err)

    tasks = [fetch_temperature(city) for city in cities]
    await asyncio.gather(*tasks)
    await client.aclose()

    return [schemas.Temperature.model_validate(record) for record in
            temperature_records]


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_all_temperatures(
        city_id: Optional[int] = None,
        db: AsyncSession = Depends(get_db_session)
):
    if city_id is not None:
        temperatures = await crud.get_temperature_by_id(city_id, db)
    else:
        temperatures = await crud.get_temperatures(db)

    return temperatures
