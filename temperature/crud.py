from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from sqlalchemy.orm import selectinload

from city.models import CityModel
from temperature.models import TemperatureModel


async def get_all_temperature(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(TemperatureModel)
        .options(selectinload(TemperatureModel.city))
        .offset(skip).limit(limit).order_by(TemperatureModel.id.desc())
    )
    temperature = result.scalars().all()
    return temperature


async def get_temperature_count(db: AsyncSession, city_id: int | None = None):
    if city_id:
        result = await db.execute(
            select(TemperatureModel)
            .where(TemperatureModel.city_id==city_id))
    else:
        result = await db.execute(select(TemperatureModel))
    return len(result.all())


async def get_temperature_by_city_id(
        db: AsyncSession,
        city_id: int,
        skip: int = 0,
        limit: int = 10
):
    result = await db.execute(
        select(TemperatureModel)
        .options(selectinload(TemperatureModel.city))
        .where(TemperatureModel.city_id==city_id)
        .offset(skip).limit(limit).order_by(TemperatureModel.id.desc())
    )
    temperature = result.scalars().all()
    return temperature


async def get_temperature(
        db: AsyncSession,
        city_id: int | None = None,
        skip: int = 0,
        limit: int = 10
):
    if city_id:
        temperature = await get_temperature_by_city_id(
            city_id=city_id,
            skip=skip,
            limit=limit,
            db=db)
        if not temperature:
            raise HTTPException(status_code=404, detail="Temperature for the given CITY_ID was not found.")
    else:
        temperature = await get_all_temperature(
            skip=skip,
            limit=limit,
            db=db
        )
    return temperature


async def fetch_temperature_for_city(city_name: str) -> float:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://wttr.in/{city_name}?format=%t", timeout=10)
            response.raise_for_status()
            temp = response.text.strip().replace("°C", "").replace("+", "")
            return float(temp)
    except Exception as e:
        print(f"Error fetching temperature for {city_name}: {e}")
        return None


async def create_temperature(
        db: AsyncSession,
        city: CityModel,
        temperature: float
):
    temp = TemperatureModel(
        city_id=city.id,
        temperature=temperature,
        date_time=datetime.now(timezone.utc)
    )
    db.add(temp)
    await db.commit()
    await db.refresh(temp)
    return temp
