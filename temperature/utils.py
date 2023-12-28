from sqlalchemy.ext.asyncio import AsyncSession
import datetime
import asyncio
import aiohttp

from . import schemas, crud
from city import crud as city_crud
from city import schemas as city_schemas
from settings import settings


async def get_response_data(
    session: aiohttp.ClientSession,
    city: city_schemas.City
):
    async with session.get(
        url=settings.WEATHER_URL,
        headers=settings.HEADERS,
        params={
            "q": city.name
        },
    ) as resp:
        data = await resp.json()
        return schemas.TemperatureCreate(
            city_id=city.id,
            date_time=datetime.datetime.now(),
            temperature=data["current"]["temp_c"]
        )


async def create_temperature(db: AsyncSession) -> None:
    tasks = []

    async with aiohttp.ClientSession() as session:

        for city in await city_crud.get_all_cities(db=db):
            tasks.append(
                asyncio.ensure_future(
                    get_response_data(session, city)
                )
            )

        temperatures = await asyncio.gather(*tasks)

    for temperature in temperatures:
        await crud.create_temperature(db=db, temperature=temperature)
