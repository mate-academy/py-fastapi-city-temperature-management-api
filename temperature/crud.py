from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
import os
import httpx
from dotenv import load_dotenv

from database import get_db
from models import Temperature


load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = os.getenv("BASE_URL")


async def fetch_temperature(city_name: str) -> float | None:
    params = {
        "q": city_name,
        "units": "metric",
        "appid": API_KEY,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(BASE_URL, params=params)

    if response.status_code != 200:
        return None

    data = response.json()
    main_data = data.get("main", {})
    return main_data.get("temp")


async def get_cities_temperature_or_by_city_id(
        city_id: int | None = None,
        db: AsyncSession = Depends(get_db)):
    stmt = (select(Temperature).options(selectinload(Temperature.city)))
    if city_id:
        stmt = stmt.where(Temperature.city_id == city_id)
    result = await db.execute(stmt)
    temperature = result.scalars().all()

    return temperature
