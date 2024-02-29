import asyncio
import os
from datetime import datetime

import aiohttp
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from city.crud import get_all_cities
from dependencies import get_db
from temperature import crud, schemas

api_key = os.getenv("WEATHER_API_KEY")

router = APIRouter()


async def fetch_temperature(city_name, api_key):
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city_name}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                current = data.get('current')
                if current:
                    return current.get('temp_c')
            return None


@router.post("/update/")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = get_all_cities(db)
    tasks = []

    for city in cities:
        tasks.append(fetch_temperature(city.name, api_key))

    temperatures = await asyncio.gather(*tasks)

    for city, temperature in zip(cities, temperatures):
        if temperature:
            db_temperature = schemas.TemperatureCreate(
                date_time=datetime.now(),
                temperature=temperature,
                city_id=city.id
            )
            crud.create_temperature(db=db, temperature=db_temperature)

    return {"message": "Temperatures updated successfully"}


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(db: Session = Depends(get_db),
                      ) -> list[schemas.Temperature]:
    return crud.get_all_temperatures(db=db)


@router.get("/temperatures/{city_id}/", response_model=list[schemas.Temperature])
def read_temperatures_by_city(city_id: int,
                              db: Session = Depends(get_db),
                              ) -> list[schemas.Temperature]:
    return crud.get_temperatures_by_city(db=db, city_id=city_id)
