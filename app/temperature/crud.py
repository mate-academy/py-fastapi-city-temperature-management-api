import os

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv

from app.temperature.models import Temperature


load_dotenv()


async def get_temperature_list(
    db: AsyncSession,
    city_id: int | None = None
) -> list[Temperature]:
    stmt = select(Temperature)

    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)

    result = await db.execute(stmt)

    return list(result.scalars().all())


async def parse_temperature_from_api_by_name(
    client: httpx.AsyncClient,
    city_name: str
) -> str:
    url = "https://api.tomorrow.io/v4/weather/realtime"
    response = await client.get(
        url,
        params={
            "apikey": os.getenv("API_KEY"),
            "location": city_name
        }
    )

    return str(response.json()["data"]["values"]["temperature"])
