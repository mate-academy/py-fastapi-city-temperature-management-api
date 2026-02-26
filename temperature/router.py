from datetime import datetime
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud
from settings import settings
from city import crud as city_crud

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)], city_id: int | None = None
):
    if city_id:
        return await crud.get_temperatures_by_city_id(db=db, city_id=city_id)
    return await crud.get_all_temperatures(db=db)


@router.post("/temperatures/update", response_model=list[schemas.Temperature])
async def update_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    cities = await city_crud.get_all_cities(db=db)
    results = []
    async with httpx.AsyncClient() as client:
        for city in cities:
            url = (
                f"https://api.openweathermap.org/data/2.5/weather?"
                f"q={city.name}&"
                f"appid={settings.WEATHER_API_KEY}"
                f"&units=metric"
            )
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                db_temperature = await crud.create_temperature(
                    db=db,
                    temperature=schemas.TemperatureCreate(
                        city_id=city.id,
                        date_time=datetime.now(),
                        temperature=data["main"]["temp"],
                    ),
                )
                results.append(db_temperature)
            except (httpx.HTTPStatusError, httpx.RequestError, KeyError):
                continue

    return results
