import os

from datetime import datetime
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from dotenv import load_dotenv
from city.models import City
from . import models

load_dotenv()

API_KEY = os.environ.get("API_KEY")
URL = "http://api.weatherapi.com/v1/current.json"


async def get_temperatures(
    db: AsyncSession,
    city_id: int | None = None,
) -> list[models.Temperature]:
    query = select(models.Temperature)

    if city_id:
        query = query.where(models.Temperature.city_id == city_id)

    list = await db.execute(query)

    return list.scalars().all()


async def update_temperatures(db: AsyncSession) -> None:
    list = await db.execute(select(City))
    cities = list.scalars().all()

    async with AsyncClient() as client:
        for city in cities:
            request = await client.get(
                URL,
                params={"key": API_KEY, "q": city.name}
            )

            if request.status_code == 200:
                current = request.json().get("current")
                temperature = current.get("temp_c")
                date_time = datetime.strptime(
                    current.get("last_updated"),
                    "%Y-%m-%d %H:%M"
                )

                db.add(models.Temperature(
                    temperature=temperature,
                    date_time=date_time,
                    city_id=city.id,
                ))

    await db.commit()
