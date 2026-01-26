from datetime import datetime

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util.concurrency import asyncio

from cities.models import DBCity
from database import SessionLocal
from temperatures import models
from settings import settings


async def create_temperature(
        db: AsyncSession,
        city_id: int,
        temperature: float
) -> models.DBTemperature:
    db_temperature = models.DBTemperature(
        city_id=city_id,
        date_time=datetime.now(),
        temperature=temperature,
    )

    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)

    return db_temperature


async def create_url_get_temperature(city: DBCity) -> dict:
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": settings.WEATHER_API_KEY,
        "q": city.name,
        "aqi": "no"
    }

    return {"url": url, "params": params, "city_id": city.id}


async def send_request_get_temperature(data: dict, client: httpx.AsyncClient) -> float:
    response = await client.get(url=data["url"], params=data["params"])
    response_data = response.json()
    temp_c = response_data.get("current", {}).get("temp_c", None)

    if temp_c is None:
        raise ValueError("Temperature data not found in response")

    return temp_c


async def create_temperatures(city: DBCity, client: httpx.AsyncClient) -> None:
    async with SessionLocal() as db:
        url = await create_url_get_temperature(city)
        temp_in_city = await send_request_get_temperature(url, client)
        await create_temperature(db=db, city_id=url["city_id"], temperature=temp_in_city)


async def update_temperature(db: AsyncSession) -> None:
    result = await db.execute(select(DBCity))
    cities = result.scalars().all()

    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            for city in cities:
                tg.create_task(create_temperatures(city=city, client=client))


async def get_all_temperatures(db: AsyncSession, city_id: int | None = None) -> list[models.DBTemperature]:
    stmt = select(models.DBTemperature)

    if city_id is not None:
        stmt =stmt.where(models.DBTemperature.city_id == city_id)

    result = await db.scalars(stmt)

    return result.all()
