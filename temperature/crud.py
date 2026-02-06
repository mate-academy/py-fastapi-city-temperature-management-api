from asyncio import TaskGroup
from datetime import datetime
from typing import Any

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import DBCity
from dependencies import paginate
from settings import settings
from temperature.models import DBTemperature


async def get_temperatures(
        db: AsyncSession,
        page: int = 1,
        size: int = 10,
        city_id: int = None
) -> dict[str, Any]:
    query = select(DBTemperature)
    if city_id is not None:
        query = query.where(DBTemperature.city_id == city_id)
    return await paginate(db=db, query=query, page=page, size=size)


async def send_requests(
        db: AsyncSession,
        city: DBCity,
        client: AsyncClient
) -> None:
    try:
        response = await client.get(
            "http://api.weatherapi.com/v1/current.json",
            params={
                "key": settings.WEATHER_API_KEY,
                "q": city.name,
                "aqi": "no"
            }
        )
        response.raise_for_status()
        data = response.json()

        update_map = {
            "temperature": data["current"]["temp_c"],
            "date_time": datetime.strptime(data["current"]["last_updated"],
                                           "%Y-%m-%d %H:%M")
        }

        db.add(DBTemperature(city_id=city.id, **update_map))

    except Exception as e:
        print(f"Error updating {city.name}: {e}")


async def fetch_and_update_temperature(db: AsyncSession) -> dict[str, Any]:
    result = await db.execute(select(DBCity))
    db_cities = result.scalars().all()
    async with AsyncClient() as client:
        async with TaskGroup() as tg:
            [
                tg.create_task(send_requests(db, city, client))
                for city in db_cities
            ]
    await db.commit()
    return await get_temperatures(db)
