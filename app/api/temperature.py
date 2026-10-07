import asyncio

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.crud import city as crud_city
from app.crud import temperature as crud_temperature
from app.schemas.temperature import Temperature, TemperatureCreate

router = APIRouter(prefix="/temperatures", tags=["temperatures"])

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_temperature(client: httpx.AsyncClient, city_name: str) -> float:
    geo_response = await client.get(
        GEOCODING_URL,
        params={"name": city_name, "count": 1},
    )
    geo_response.raise_for_status()
    results = geo_response.json().get("results")
    if not results:
        raise ValueError(f"City '{city_name}' was not found")

    weather_response = await client.get(
        FORECAST_URL,
        params={
            "latitude": results[0]["latitude"],
            "longitude": results[0]["longitude"],
            "current": "temperature_2m",
        },
    )
    weather_response.raise_for_status()
    return float(weather_response.json()["current"]["temperature_2m"])


@router.get("", response_model=list[Temperature])
async def read_temperatures(
        city_id: int | None = None,
        db: AsyncSession = Depends(get_db),
):
    if city_id is not None and await crud_city.get_city(db, city_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    return await crud_temperature.get_temperatures(db, city_id)


@router.post("/update", response_model=list[Temperature])
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await crud_city.get_cities(db)

    async with httpx.AsyncClient(timeout=10.0) as client:
        results = await asyncio.gather(
            *(fetch_temperature(client, city.name) for city in cities),
            return_exceptions=True,
        )

    temperatures = [
        TemperatureCreate(city_id=city.id, temperature=result)
        for city, result in zip(cities, results)
        if not isinstance(result, BaseException)
    ]

    if cities and not temperatures:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not fetch temperature for any city",
        )

    return await crud_temperature.bulk_create_temperatures(db, temperatures)
