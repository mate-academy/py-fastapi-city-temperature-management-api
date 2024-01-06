from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import asyncio
import aiohttp

from settings import settings
from city.schemas import City
from city.crud import get_all_cities
from . import schemas, crud


async def read_temperatures_from_api(
    session: aiohttp.ClientSession, city: City
) -> schemas.TemperatureCreate | None:
    request_parameters = {
        "q": city.name,
        "appid": settings.WEATHER_API_KEY,
        "units": "metric",
    }
    async with session.get(
        url=settings.WEATHER_API_URL,
        params=request_parameters,
    ) as response:
        data = await response.json()
        return schemas.TemperatureCreate(
            city_id=city.id,
            date_time=datetime.utcnow() + timedelta(
                seconds=data.get("timezone", 0)
            ),
            temperature=round(data["main"]["temp"], 1),
        )


async def gather_temperatures(db: AsyncSession) -> None:
    tasks = []

    async with aiohttp.ClientSession() as session:
        for city in await get_all_cities(db=db):
            tasks.append(
                asyncio.ensure_future(
                    read_temperatures_from_api(session=session, city=city)
                )
            )

        temperatures = await asyncio.gather(*tasks)

    for temperature in temperatures:
        await crud.update_temperatures(db=db, temperature=temperature)
