import asyncio
from datetime import datetime

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import city as city_model
from app.models import temperature as temp_model


async def _fetch_weather(
        client: httpx.AsyncClient,
        city: city_model.City
) -> float | None:
    try:
        url = f"https://wttr.in/{city.name}?format=j1"
        response = await client.get(url, timeout=10.0)
        if response.status_code != 200:
            return None
        data = response.json()
        temp_c = data["current_condition"][0]["temp_C"]
        return float(temp_c)
    except Exception as e:
        print(f"Failed to fetch weather for {city.name}: {e}")
        return None

async def update_all_temperatures(
        db: Session
) -> list[temp_model.Temperature]:
    cities = list(db.scalars(select(city_model.City)).all())
    if not cities:
        return []
    async with httpx.AsyncClient() as client:
        tasks = [_fetch_weather(client, city) for city in cities]
        results = await asyncio.gather(*tasks)
    new_records = []
    current_time = datetime.now()
    for city, temp in zip(cities, results):
        if temp is not None:
            new_temp = temp_model.Temperature(
                city_id=city.id,
                date_time=current_time,
                temperature=temp
            )
            db.add(new_temp)
            new_records.append(new_temp)
    if new_records:
        db.commit()
        for record in new_records:
            db.refresh(record)
    return new_records


def get_temperatures(
        db: Session,
        city_id: int | None = None
) -> list[temp_model.Temperature]:
    stmt = select(temp_model.Temperature)
    if city_id is not None:
        stmt = stmt.where(temp_model.Temperature.city_id == city_id)
    return list(db.scalars(stmt))
