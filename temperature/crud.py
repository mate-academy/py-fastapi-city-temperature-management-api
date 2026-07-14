from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
import aiohttp

from temperature.models import Temperature
from city.models import City


async def fetch_temperature(city_name: str) -> float | None:
    url = f"https://wttr.in/{city_name}?format=j1"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            data = await response.json()
            return float(data["current_condition"][0]["temp_C"])


async def update_temperatures(db: Session) -> list[Temperature]:
    cities = list(db.execute(select(City)).scalars().all())
    results = []

    for city in cities:
        temp = await fetch_temperature(city.name)
        if temp is None:
            continue
        db_temp = Temperature(
            city_id=city.id,
            date_time=datetime.utcnow(),
            temperature=temp,
        )
        db.add(db_temp)
        results.append(db_temp)

    db.commit()
    for r in results:
        db.refresh(r)
    return results


def get_temperatures(db: Session, city_id: int | None = None) -> list[Temperature]:
    query = select(Temperature)
    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)
    return list(db.execute(query).scalars().all())
