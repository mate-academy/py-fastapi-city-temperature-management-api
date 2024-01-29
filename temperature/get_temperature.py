import os

import httpx
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models

load_dotenv()

USER_API_KEY = os.environ["USER_API_KEY"]
URL = "https://api.weatherapi.com/v1/current.json"


async def get_city_temperatures(db: AsyncSession) -> dict:
    """
    Do not use the "get_all_cities" function
     from "cities.crud" for the "cities" variable.
     The "cities" variable, in this case,
      takes the "Coroutine" type, not "Iterable".
    """

    cities = (
        await db.execute(select(models.City))).scalars().all()
    city_temp = {}

    async with httpx.AsyncClient() as client:
        for city in cities:
            params = {"key": USER_API_KEY, "q": city.name, "aqi": "no"}

            response_data = (await client.get(URL, params=params)).json()
            city_temp[city.id] = response_data
            print(city_temp[city.id])
    return city_temp
