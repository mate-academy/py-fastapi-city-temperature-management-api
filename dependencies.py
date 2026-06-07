import os
from typing import AsyncGenerator

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from city import models
from databese import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


URL = "http://api.weatherapi.com/v1/current.json"


async def get_city_temperature(
    client: httpx.AsyncClient, city_name: str
) -> float:

    payload_params = {
        "q": city_name,
        "key": os.getenv("WEATHER_API_KEY"),
    }

    response = await client.get(URL, params=payload_params)
    data = response.json()
    try:
        return data["current"]["temp_c"]
    except KeyError:
        raise ValueError(f"City '{city_name}' not found")
