from datetime import datetime
from fastapi import HTTPException
import httpx
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud as city_crud
from city import models as city_models
from temperature import models


# Better move it to .env
API_KEY = "afbf9689ace991585a54c963b9ded14c"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


async def fetch_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            BASE_URL,
            params={"q": city_name, "appid": API_KEY, "units": "metric"},
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Error fetching data for city {city_name}",
            )
        data = response.json()
        return data["main"]["temp"]


async def get_all_temperatures_records(
        db: AsyncSession,
) -> list[models.DBTemperature]:
    result = await db.execute(select(models.DBTemperature))
    return list(result.scalars().all())


async def get_all_temperatures_records_by_city_id(
        db: AsyncSession,
        city_id: int,
) -> list[models.DBTemperature]:
    city = await city_crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    result = await db.execute(
        select(models.DBTemperature).
        filter(models.DBTemperature.city_id == city_id)
    )
    return list(result.scalars().all())


async def update_temperatures(db: AsyncSession) -> None:
    result = await db.execute(select(city_models.DBCity))
    cities = result.scalars().all()

    if not cities:
        raise HTTPException(
            status_code=404,
            detail="No cities found in the database",
        )

    for city in cities:
        temp = await fetch_temperature(city.name)
        new_temperature = models.DBTemperature(
            city_id=city.id,
            temperature=temp,
            date_time=datetime.now(),
        )
        db.add(new_temperature)

    await db.commit()
