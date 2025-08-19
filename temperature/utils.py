from typing import Dict, Optional

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import CityModel
from settings import get_settings

settings = get_settings()


async def fetch_weather(city: str) -> Optional[Dict]:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                settings.BASE_WEATHER_URL,
                params={"key": settings.WEATHER_API_KEY, "q": city},
            )
            response.raise_for_status()

            data = response.json()

            city_name = data.get("location", {}).get("name")
            temperature = data.get("current", {}).get("temp_c")

            if city_name is None or temperature is None:
                return None

            return {"city": city_name, "temperature": temperature}

    except (httpx.RequestError, httpx.HTTPStatusError, ValueError):
        return None


async def get_cities_id_and_name(db: AsyncSession) -> list[tuple[int, str]]:
    query = select(CityModel.id, CityModel.name)
    result = await db.execute(query)
    return result.all()
