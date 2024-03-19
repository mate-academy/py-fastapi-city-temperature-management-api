import httpx
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from pydantic import ValidationError

from city.crud import get_all_cities
from settings import settings
from city.models import DBCity
from .models import DBTemperature
from .schemas import CreateTemperature

# stop and limit for pagination
STOP, LIMIT = 0, 10


async def request_city_temp(
        city: DBCity,
        client: httpx.AsyncClient
) -> dict:
    """ Make request to get temperature, base on city name """
    response = (
        await client.get(
            settings.CURRENT_WEATHER_URL,
            params={"q": city.name, "key": settings.WEATHER_API_KEY}
        )
    ).json()

    extracted_fields = {
        "city_id": city.id,
        "date_time": response["current"].get("last_updated"),
        "temp_c": response["current"].get("temp_c"),
        "temp_f": response["current"].get("temp_f")
    }
    return extracted_fields


async def validate_temp(city_temp: dict) -> dict:
    """
    Validata/convert the data using Pydantic model and
    keeping a data integrity
    """
    try:
        return CreateTemperature(**city_temp).model_dump()

    except ValidationError as e:
        print(e)
        return {}


async def fetch_temperatures(db: AsyncSession):
    """Retrieve temperatures"""
    stop, limit = STOP, LIMIT
    cities = await get_all_cities(db=db)

    while limit <= len(cities):
        async with httpx.AsyncClient() as client:
            yield await asyncio.gather(
                *[
                    request_city_temp(city=city, client=client)
                    for city in cities[stop: stop + limit]
                ]
            )
            stop, limit = limit, limit + LIMIT


async def save_temperatures(db: AsyncSession, temperatures_dict):
    query = insert(DBTemperature)
    valid_temperatures = [temp for temp in temperatures_dict if temp]

    if valid_temperatures:
        # ORM Bulk INSERT
        await db.execute(
            query,
            *valid_temperatures
        )
        await db.commit()


async def scrape_temperatures(db: AsyncSession) -> None:
    # fetch and validate the temperatures data
    temperatures = await asyncio.gather(
        *[
            validate_temp(temp_dict)
            async for temp_dict in fetch_temperatures(db=db)
        ]
    )
    await save_temperatures(db=db, temperatures_dict=temperatures)
