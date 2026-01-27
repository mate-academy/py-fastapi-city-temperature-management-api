from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import httpx
import asyncio
from app import schemas, crud, models
from app.database import get_db

router = APIRouter(
    prefix="/temperatures",
    tags=["temperatures"]
)


async def fetch_temperature_for_city(city_name: str) -> Optional[float]:
    """Fetch current temperature from Open-Meteo API."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
            geocode_params = {
                "name": city_name,
                "count": 1,
                "language": "en",
                "format": "json"
            }

            geocode_response = await client.get(geocode_url, params=geocode_params)
            geocode_response.raise_for_status()
            geocode_data = geocode_response.json()

            if not geocode_data.get("results"):
                return None

            latitude = geocode_data["results"][0]["latitude"]
            longitude = geocode_data["results"][0]["longitude"]

            weather_url = "https://api.open-meteo.com/v1/forecast"
            weather_params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": "true"
            }

            weather_response = await client.get(weather_url, params=weather_params)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            current_weather = weather_data.get("current_weather", {})
            temperature = current_weather.get("temperature")

            return temperature

    except (httpx.HTTPError, KeyError, IndexError) as e:
        print(f"Error fetching temperature for {city_name}: {e}")
        return None


@router.post("/update", response_model=schemas.TemperatureUpdateResponse)
async def update_temperatures(db: Session = Depends(get_db)):
    """Fetch and store current temperature for all cities."""
    cities = crud.get_cities(db=db, skip=0, limit=1000)

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found in database")

    tasks = [fetch_temperature_for_city(city.name) for city in cities]
    temperatures = await asyncio.gather(*tasks)

    updated_cities = []
    updated_count = 0
    current_time = datetime.utcnow()

    for city, temperature in zip(cities, temperatures):
        if temperature is not None:
            temp_create = schemas.TemperatureCreate(
                city_id=city.id,
                temperature=temperature,
                date_time=current_time
            )
            crud.create_temperature(db=db, temperature=temp_create)
            updated_cities.append(city.name)
            updated_count += 1

    return schemas.TemperatureUpdateResponse(
        message=f"Successfully updated temperatures for {updated_count} out of {len(cities)} cities",
        updated_count=updated_count,
        cities=updated_cities
    )


@router.get("", response_model=List[schemas.Temperature])
def read_temperatures(
        city_id: Optional[int] = Query(None, description="Filter by city ID"),
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    """Get temperature records."""
    temperatures = crud.get_temperatures(db=db, city_id=city_id, skip=skip, limit=limit)
    return temperatures
