import asyncio
from typing import List

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from city.crud import get_cities
from city.models import City
from dependencies import get_db
from temperature import schemas, crud
from temperature.crud import create_temperature
from temperature.schemas import TemperatureCreate

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


async def fetch_temperature_for_city(city: City) -> float | None:
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city.name, "count": 1, "language": "en"}

    async with httpx.AsyncClient() as client:
        try:
            geo_response = await client.get(geo_url, params=params)
            geo_response.raise_for_status()
        except httpx.HTTPError:
            return None

    geo_data = geo_response.json()
    if not geo_data.get("results"):
        return None

    lat = geo_response.json()["results"][0]["latitude"]
    lon = geo_response.json()["results"][0]["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m",
        "timezone": "UTC",
    }
    try:
        weather_response = await client.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
    except httpx.HTTPError:
        return None

    return weather_response.json()["current"]["temperature_2m"]


@router.post("/update", status_code=status.HTTP_202_ACCEPTED)
async def update_all_temperatures(db: Session = Depends(get_db)):
    cities = get_cities(db=db, skip=0, limit=1000)
    if not cities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )

    tasks = [fetch_temperature_for_city(city) for city in cities]
    temperatures = await asyncio.gather(*tasks, return_exceptions=True)

    created_count = 0
    for city, temp in zip(cities, temperatures):
        if isinstance(temp, float):
            temp_create = TemperatureCreate(city_id=city.id, temperature=temp)
            create_temperature(db=db, temp_in=temp_create)
            created_count += 1

    return {"message": f"Updated temperatures for {len(cities)} cities"}


@router.get("/", response_model=List[schemas.Temperature])
def read_all_temperatures(
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if city_id is not None:
        return crud.get_temperature_by_city(
            db=db, city_id=city_id, skip=skip, limit=limit
        )
    return crud.get_temperatures(db=db, skip=skip, limit=limit)
