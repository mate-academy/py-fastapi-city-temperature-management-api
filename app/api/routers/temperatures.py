import asyncio
from datetime import datetime, timezone

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.city import list_cities
from app.crud.temperature import create_temperature, list_temperatures
from app.db.session import get_db
from app.schemas.temperature import TemperatureRead

router = APIRouter(prefix="/temperatures")


async def fetch_current_temperature(client: httpx.AsyncClient, *, lat: float, lon: float) -> float:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m",
    }
    r = await client.get(url, params=params)
    r.raise_for_status()
    data = r.json()
    try:
        return float(data["current"]["temperature_2m"])
    except (KeyError, TypeError, ValueError) as e:
        raise RuntimeError("Unexpected response schema from temperature provider") from e


@router.post("/update", status_code=status.HTTP_201_CREATED)
async def update_temperatures(db: AsyncSession = Depends(get_db)) -> dict:
    cities = await list_cities(db)
    if not cities:
        raise HTTPException(status_code=400, detail="No cities found. Create cities first.")

    timeout = httpx.Timeout(settings.OPEN_METEO_TIMEOUT_SECONDS)
    async with httpx.AsyncClient(timeout=timeout) as client:
        async def job(city):
            temp_value = await fetch_current_temperature(client, lat=city.latitude, lon=city.longitude)
            await create_temperature(db, city_id=city.id, temperature=temp_value, date_time=datetime.now(timezone.utc))
            return city.id, temp_value

        results = []
        for coro in asyncio.as_completed([job(c) for c in cities]):
            results.append(await coro)

    return {"updated": len(results), "results": [{"city_id": cid, "temperature": t} for cid, t in results]}


@router.get("", response_model=list[TemperatureRead])
async def list_temperatures_endpoint(
    city_id: int | None = Query(default=None, description="Filter by city id"),
    db: AsyncSession = Depends(get_db),
) -> list[TemperatureRead]:
    return await list_temperatures(db, city_id=city_id)
