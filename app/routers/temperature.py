from typing import Optional
import asyncio
import httpx

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Query
)
from fastapi.concurrency import run_in_threadpool

from app.schemas.temperature import TemperatureCreate, TemperatureRead
from app.repositories import TemperatureRepository, CityRepository
from app.dependencies import get_temperature_repository, get_city_repository

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


async def fetch_temperature_for_city(city_name: str) -> Optional[float]:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
            geocoding_params = {
                "name": city_name,
                "count": 1,
                "language": "en",
                "format": "json",
            }

            geo_response = await client.get(geocoding_url, params=geocoding_params)
            geo_response.raise_for_status()
            geo_data = geo_response.json()

            if not geo_data.get("results"):
                return None

            latitude = geo_data["results"][0]["latitude"]
            longitude = geo_data["results"][0]["longitude"]

            weather_url = "https://api.open-meteo.com/v1/forecast"
            weather_params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": "true",
            }

            weather_response = await client.get(weather_url, params=weather_params)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            return weather_data.get("current_weather", {}).get("temperature")

    except Exception:
        return None


@router.post("/update", status_code=status.HTTP_201_CREATED)
async def update_temperatures(
    city_repo: CityRepository = Depends(get_city_repository),
    temp_repo: TemperatureRepository = Depends(get_temperature_repository),
):
    cities = await run_in_threadpool(city_repo.get_all)

    if not cities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cities found in database",
        )

    tasks = [fetch_temperature_for_city(city.name) for city in cities]
    temperatures = await asyncio.gather(*tasks)

    temperature_records = []
    successful_cities = []
    failed_cities = []

    for city, temp in zip(cities, temperatures):
        if temp is not None:
            temperature_records.append(
                TemperatureCreate(city_id=city.id, temperature=temp)
            )
            successful_cities.append(city.name)
        else:
            failed_cities.append(city.name)

    if temperature_records:
        await run_in_threadpool(
            temp_repo.create_bulk,
            temperature_records,
        )

    return {
        "message": "Temperature update completed",
        "total_cities": len(cities),
        "successful_updates": len(successful_cities),
        "failed_updates": len(failed_cities),
        "successful_cities": successful_cities,
        "failed_cities": failed_cities,
    }


@router.get("/", response_model=list[TemperatureRead])
def get_temperatures(
        city_id: Optional[int] = Query(None, description="Filter by city ID"),
        skip: int = 0,
        limit: int = 100,
        city_repo: CityRepository = Depends(get_city_repository),
        temp_repo: TemperatureRepository = Depends(get_temperature_repository),
):
    if city_id is not None:
        city = city_repo.get_by_id(city_id)
        if not city:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City with id {city_id} not found",
            )
        temperatures = temp_repo.get_by_city_id(city_id, skip, limit)
    else:
        temperatures = temp_repo.get_all(skip, limit)

    return temperatures