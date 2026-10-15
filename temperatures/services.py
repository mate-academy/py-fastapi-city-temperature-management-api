import asyncio
from datetime import datetime, timezone

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from cities.crud import get_cities
from temperatures import crud
from temperatures.models import Temperature
from weather_api.weather import fetch_temperature


async def update_temperatures(db: AsyncSession) -> dict:
    cities = await get_cities(db=db)

    async with httpx.AsyncClient(timeout=10.0) as client:
        results = await asyncio.gather(
            *(fetch_temperature(client, city.name) for city in cities),
            return_exceptions=True,
        )

    now = datetime.now(timezone.utc)
    new_records = []
    updated = []
    failed = []

    for city, result in zip(cities, results):
        if isinstance(result, Exception):
            failed.append({"city": city.name, "error": str(result)})
            continue
        new_records.append(
            Temperature(city_id=city.id, date_time=now, temperature=result)
        )
        updated.append(city.name)

    if new_records:
        await crud.create_temperatures(db, new_records)

    return {"updated": updated, "failed": failed}
