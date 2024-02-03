import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from city import models
from settings import settings

api_key = settings.API_KEY
url = settings.WEATHER_API_URL


async def fetch_current_temperature_and_time_for_cities(db: AsyncSession) -> dict:
    query = select(models.CityDB)
    result = await db.execute(query)
    cities_list = result.scalars().all()

    city_temp = {}
    async with httpx.AsyncClient() as session:
        for city in cities_list:
            params = {"key": api_key, "q": city.name, "aqi": "no"}
            response = await session.get(url=url, params=params)
            response_data = response.json()
            if "error" in response_data:
                print(f"No {city.name} location found")
                continue
            city_temp[city.id] = response_data
    return city_temp
