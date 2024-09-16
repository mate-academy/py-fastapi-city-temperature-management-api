from datetime import datetime

import httpx
from httpx import AsyncClient
from sqlalchemy import select, insert, CursorResult

from sqlalchemy.ext.asyncio import AsyncSession

from city import models as city_models
from settings import settings
from temperature import models as temperature_models


async def get_city_weather(
        client: AsyncClient,
        city: city_models.City,
        raise_exception: bool | None = None
) -> temperature_models.Temperature | None:

    params = {"key": settings.API_KEY, "q": city.name, "aqi": "no"}

    response = await client.get(settings.URL, params=params)

    if raise_exception:
        response.raise_for_status()

    if response.status_code != httpx.codes.OK:
        return None

    result = response.json()

    if (temp_c := result.get("current", {}).get("temp_c")) is None:
        return None

    if (last_updated := result.get("current", {}).get("last_updated")) is None:
        return None
    date_time = datetime.strptime(last_updated, "%Y-%m-%d %H:%M")
    print(city.name, temp_c, date_time)

    city_temp = temperature_models.Temperature(date_time=date_time, temperature=temp_c, city_id=city.id)
    return city_temp


async def is_exist_city_temperature(db: AsyncSession, city_temp: temperature_models.Temperature) -> bool:
    query = select(temperature_models.Temperature).where(
        temperature_models.Temperature.city_id == city_temp.city_id,
        temperature_models.Temperature.date_time == city_temp.date_time
    )
    cities_temp_list = await db.execute(query)
    return cities_temp_list.scalar() is not None


async def add_temperature(db: AsyncSession, city_temp: temperature_models.Temperature) -> CursorResult:
    query = insert(temperature_models.Temperature).values(
        temperature=city_temp.temperature,
        city_id=city_temp.city_id,
        date_time=city_temp.date_time
    )
    return await db.execute(query)
