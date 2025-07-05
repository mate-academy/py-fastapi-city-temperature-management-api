from typing import List

import httpx
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from city.crud import get_city_by_id, get_cities
from dependencies import get_db
from settings import settings
from temperature import crud
from temperature.schemas import (
    TemperatureResponse,
    TemperatureRequest,
    TemperatureDetailResponse,
)

temperature = APIRouter(prefix="/temperatures")


@temperature.get("/", response_model=List[TemperatureDetailResponse])
async def get_temperatures(
    city_id: int | None = Query(None, ge=1), db: AsyncSession = Depends(get_db)
):
    result = await crud.get_temperature(db, city_id)
    if not result:
        raise HTTPException(status_code=404, detail="Temperatures not found")
    return result


# @temperature.post("/", response_model=TemperatureResponse)
# async def create_temperature(
#     data: TemperatureRequest, db: AsyncSession = Depends(get_db)
# ):
#     if not await get_city_by_id(db, data.city_id):
#         raise HTTPException(status_code=404, detail="City not found")
#     temperature_ = await crud.create_temperature(db, data)
#     if not temperature_:
#         raise HTTPException(status_code=400, detail="Temperature already exists")
#     return temperature_


async def fetch_temperatures(db: AsyncSession = Depends(get_db)):
    results = []
    cities = await get_cities(db)
    cities = {(city.id, city.name) for city in cities}
    url = settings.WEATHER_API_URL
    key = settings.WEATHER_API_KEY

    async with httpx.AsyncClient() as client:
        try:
            for city in cities:
                response = await client.get(
                    f"{url}",
                    params={"q": city[1], "key": key},
                )
                response.raise_for_status()
                data = response.json()["current"]
                results.append(
                    TemperatureRequest(
                        city_id=city[0],
                        date_time=data["last_updated"],
                        temperature=data["temp_c"],
                    )
                )
        except httpx.HTTPError:
            raise HTTPException(status_code=500, detail="Something went wrong")

    return results


@temperature.post("/update", response_model=List[TemperatureResponse])
async def update_temperatures(
    data: List[TemperatureRequest] = Depends(fetch_temperatures),
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_temperatures(db, data)
