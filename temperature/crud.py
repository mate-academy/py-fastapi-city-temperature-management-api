from datetime import datetime

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from starlette.exceptions import HTTPException

from .models import Temperature


async def fetch_temperature_by_city(city_name: str) -> str:
    url = f"https://wttr.in/{city_name}?format=%t"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            temperature = response.text.strip()
            return str(temperature)
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error fetching temperature data for {city_name}: {e.response.text}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching data for {city_name}: {str(e)}")


async def get_all_temperatures(db: AsyncSession):
    query = select(Temperature).options(selectinload(Temperature.city))
    result = await db.execute(query)
    temperatures = result.scalars().all()
    return temperatures


async def get_temperatures_by_city(city_id: int, db: AsyncSession):
    query = select(Temperature).where(Temperature.city_id == city_id).options(selectinload(Temperature.city))
    result = await db.execute(query)
    temperatures = result.scalars().all()
    return temperatures


async def create_update_temperature(temperature: str, city_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Temperature).where(Temperature.city_id == city_id))
        existing_temperature = result.scalars().first()

        if existing_temperature:
            existing_temperature.temperature = temperature
            existing_temperature.date_time = datetime.now()
        else:
            existing_temperature = Temperature(
            temperature=temperature,
            city_id=city_id,
            date_time=datetime.now()
            )
            db.add(existing_temperature)
        await db.commit()
        await db.refresh(existing_temperature)
        return existing_temperature
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
