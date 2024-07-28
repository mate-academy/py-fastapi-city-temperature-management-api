from http.client import HTTPException
from typing import Dict
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.city.models import City
from src.temperature.models import Temperature
from src.config import settings


async def get_async_client() -> AsyncClient:
    return AsyncClient()


async def fetch_temperature(
    session: AsyncSession, client: AsyncClient
) -> Dict[str, str]:
    stmt = select(City)
    cities_list = await session.execute(stmt)
    for city_tuple in cities_list.fetchall():
        city = city_tuple[0]
        res = await client.get(
            url="https://api.openweathermap.org/data/2.5/weather",
            params={
                "units": "metric",
                "q": f"{city.name}",
                "lang": "ru",
                "APPID": settings.OPENWEATHER_API_KEY,
            },
        )
        if res.status_code != 200:
            raise HTTPException("City not found")
        res = res.json()
        session.add(
            Temperature(
                city_id=city.id,
                temperature=res["main"]["temp"],
            )
        )
    await session.commit()
    return {"result": "Temperature was fetched successfully"}
