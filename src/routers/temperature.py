import asyncio

from datetime import datetime
from typing import List, Optional

from httpx import AsyncClient
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src import dependencies, schemas
from src.cruds import city_cruds, temperature_cruds
from src.db import models
from src.dependencies import get_settings
from src.settings import Settings

temperature_router = APIRouter(prefix="/temperatures")


@temperature_router.get("", response_model=List[schemas.Temperature])
async def get_by_city_id(
        city_id: Optional[int] = Query(None),
        db: AsyncSession = Depends(dependencies.get_db)
) -> List[schemas.Temperature]:
    if city_id is None:
        return await temperature_cruds.get_all(db=db)

    city = await city_cruds.get_by_id(city_id=city_id, db=db)

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return await temperature_cruds.get_by_city_id(city_id=city_id, db=db)


@temperature_router.post("/update", response_model=None)
async def create_city(
        db: AsyncSession = Depends(dependencies.get_db),
        http_client: AsyncClient = Depends(dependencies.get_http_client),
        settings: Settings = Depends(get_settings)
) -> None:
    cities: List[models.City] = await city_cruds.get_all(db=db)
    temperatures_to_create = []

    tasks = [
        temperature_cruds.get_city_temperature(
            city_name=city.name,
            http_client=http_client,
            settings=settings
        )
        for city in cities
    ]

    results: list[str] = await asyncio.gather(*tasks, return_exceptions=True)

    for city, result in zip(cities, results):
        if isinstance(result, Exception):
            print(F"Error fetching temperature for {city.name}: {result}")

        temperatures_to_create.append(schemas.TemperatureCreate(
            date_time=datetime.now(),
            temperature=int(result),
            city_id=city.id
        ))


    await temperature_cruds.create_city_temperatures(temperatures=temperatures_to_create, db=db)
