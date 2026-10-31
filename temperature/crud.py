import asyncio

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from temperature import models

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


async def get_temperatures(
    db: AsyncSession, city_id: int | None = None
) -> list[models.Temperature]:
    stmt = select(models.Temperature)
    if city_id is not None:
        stmt = stmt.where(models.Temperature.city_id == city_id)
    result = await db.scalars(stmt)
    return list(result.all())


async def fetch_temperature(client: httpx.AsyncClient, city_name: str) -> float | None:
    geo = await client.get(GEOCODING_URL, params={"name": city_name, "count": 1})
    geo.raise_for_status()
    results = geo.json().get("results")
    if not results:
        return None

    forecast = await client.get(
        FORECAST_URL,
        params={
            "latitude": results[0]["latitude"],
            "longitude": results[0]["longitude"],
            "current": "temperature_2m",
        },
    )
    forecast.raise_for_status()
    return forecast.json()["current"]["temperature_2m"]


async def update_temperatures(db: AsyncSession) -> list[models.Temperature]:
    cities = list((await db.scalars(select(City))).all())

    async with httpx.AsyncClient(timeout=10) as client:
        values = await asyncio.gather(
            *(fetch_temperature(client, c.name) for c in cities)
        )

    records = [
        models.Temperature(city_id=city.id, temperature=value)
        for city, value in zip(cities, values)
        if value is not None
    ]
    db.add_all(records)
    await db.commit()
    return records
