import asyncio
import os
from datetime import datetime

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from city.crud import get_all_cities
from dependencies import DBSessionDep, PaginationDep
from temperature import crud, schemas


load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json"

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(
    db: DBSessionDep, paginate: PaginationDep, city_id: int = None
):
    return crud.get_temperature_list(db=db, city_id=city_id, **paginate)


@router.get(
    "/temperatures/{temperature_id}", response_model=schemas.Temperature
)
def read_temperature(temperature_id: int, db: DBSessionDep):
    temperature = crud.get_temperature(db=db, temperature_id=temperature_id)

    if not temperature:
        raise HTTPException(
            status_code=404, detail="Temperature record not found"
        )

    return temperature


async def fetch_weather(city: str) -> dict:
    if not API_KEY:
        raise ValueError("API_KEY not found in environment variables.")

    try:
        url = f"{BASE_URL}?key={API_KEY}&q={city}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

            return response.json()
    except httpx.HTTPStatusError as http_err:
        raise HTTPException(
            status_code=http_err.response.status_code,
            detail="HTTP error occurred"
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


@router.post("/temperatures/update")
async def update_temperatures(db: DBSessionDep):
    cities = get_all_cities(db)

    async def fetch_and_store_temperature(city):
        weather_data = await fetch_weather(city.name)

        temperature = weather_data["current"]["temp_c"]

        temperature_data = schemas.TemperatureCreateUpdate(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=temperature
        )

        crud.create_temperature(db, temperature_data)

    tasks = [fetch_and_store_temperature(city) for city in cities]

    await asyncio.gather(*tasks)

    return {"message": "Temperatures updated successfully"}
