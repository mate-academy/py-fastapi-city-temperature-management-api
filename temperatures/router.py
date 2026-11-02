import asyncio
from datetime import datetime
from typing import List, Annotated

import httpx
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from cities.crud import get_all_cities
from dependencies import get_db
from temperatures.crud import create_temperatures, get_all_temperatures
from temperatures.schemas import (
    Temperature,
    TemperatureCreate,
    TemperatureUpdateResult,
)
from temperatures.weather_client import WeatherFetchError, fetch_current_temperature

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update/")
async def update_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[TemperatureUpdateResult]:
    cities = await get_all_cities(db)

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_current_temperature(client, city.name) for city in cities]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    now = datetime.utcnow()
    to_create: list[TemperatureCreate] = []
    response: list[TemperatureUpdateResult] = []

    for city, result in zip(cities, results):
        if isinstance(result, WeatherFetchError):
            response.append(
                TemperatureUpdateResult(
                    city_id=city.id,
                    city_name=city.name,
                    success=False,
                    error=str(result),
                )
            )
            continue
        if isinstance(result, Exception):
            response.append(
                TemperatureUpdateResult(
                    city_id=city.id,
                    city_name=city.name,
                    success=False,
                    error=f"Unexpected error: {result}",
                )
            )
            continue

        temperature: float = result
        to_create.append(
            TemperatureCreate(city_id=city.id, date_time=now, temperature=temperature)
        )
        response.append(
            TemperatureUpdateResult(
                city_id=city.id,
                city_name=city.name,
                success=True,
                temperature=temperature,
            )
        )

    if to_create:
        await create_temperatures(db, to_create)
        await db.commit()

    return response


@router.get("/", response_model=list[Temperature])
async def get_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: int | None = Query(None, alias="city_id"),
) -> List[Temperature]:
    temperatures = await get_all_temperatures(db=db, city_id=city_id)
    return [Temperature.model_validate(temp) for temp in temperatures]