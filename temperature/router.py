import asyncio
from datetime import datetime
from typing import Any, Dict, Callable, List

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from tenacity import retry, stop_after_attempt, wait_fixed

from city.models import DBCity
from database import SessionLocal
from dependencies import get_db
from settings import settings
from temperature import crud, schemas

router = APIRouter()


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def fetch_weather_data(client: httpx.AsyncClient, city_name: str) -> Dict[str, Any]:
    response = await client.get(
        settings.WEATHER_API,
        params={"key": settings.WEATHER_API_KEY, "q": city_name}
    )
    response.raise_for_status()
    return response.json()


async def handle_city_weather(client: httpx.AsyncClient, city: DBCity, db_session_factory: Callable[[], AsyncSession]) -> None:
    try:
        data = await fetch_weather_data(client, city.name)
        print(data)
        new_temperature = schemas.TemperatureCreate(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=data["current"]["temp_c"]
        )
        async with db_session_factory() as new_db_session:
            await crud.add_temperature(new_db_session, new_temperature)
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


@router.post("/temperatures/update")
async def refresh_temperatures(db: AsyncSession = Depends(get_db)) -> dict:
    cities = await crud.fetch_all_cities(db)
    limits = httpx.Limits(max_connections=10, max_keepalive_connections=5)
    timeout = httpx.Timeout(10.0, connect=60.0)

    async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
        tasks = [handle_city_weather(client, city, SessionLocal) for city in cities]
        await asyncio.gather(*tasks)

    return {"message": "Temperatures updated successfully"}

@router.get("/temperatures", response_model=list[schemas.Temperature])
async def get_all_temperatures(db: AsyncSession = Depends(get_db)) -> List[schemas.Temperature]:
    temperatures = await crud.fetch_temperatures(db)
    if not temperatures:
        raise HTTPException(status_code=404, detail="No temperatures found")
    return temperatures


@router.get("/temperatures/{city_id}", response_model=list[schemas.Temperature])
async def get_temperatures_by_city(city_id: int, db: AsyncSession = Depends(get_db)) -> List[schemas.Temperature]:
    temperatures = await crud.fetch_temperatures(db, city_id)
    if not temperatures:
        raise HTTPException(status_code=404, detail=f"No temperatures found for city ID {city_id}")
    return temperatures
