import asyncio
from datetime import datetime, timezone

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app import crud, schemas

router = APIRouter(prefix="/temperatures", tags=["temperatures"])

API_KEY = "4754d1d12975c4f0ab02a2bd003485f7"


async def fetch_temp(client: httpx.AsyncClient, city_name: str):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city_name}&units=metric&appid={API_KEY}"
    )

    try:
        response = await client.get(url, timeout=10.0)

        if response.status_code != 200:
            return None

        data = response.json()
        return data["main"]["temp"]

    except Exception:
        return None


@router.post("/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await crud.get_cities(db)

    if not cities:
        return {"saved": 0, "failed": 0}

    async with httpx.AsyncClient() as client:
        tasks = [fetch_temp(client, city.name) for city in cities]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    saved = 0
    failed = 0

    for city, result in zip(cities, results):
        if isinstance(result, Exception) or result is None:
            failed += 1
            continue

        temp_schema = schemas.TemperatureCreate(
            city_id=city.id,
            date_time=datetime.now(timezone.utc),
            temperature=float(result)
        )

        await crud.create_temperature(db, temp_schema)
        saved += 1

    return {"saved": saved, "failed": failed}


@router.get("/", response_model=list[schemas.TemperatureOut])
async def read_temperatures(
    city_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await crud.get_temperatures(db=db, city_id=city_id)