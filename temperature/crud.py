from datetime import datetime, UTC
from typing import List

from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import CityModel
from city.schemas import CityDetailSchema
from temperature.models import TemperatureModel
from temperature.schemas import TemperatureDetailSchema
from temperature.services import fetch_temperature_by_city_name


async def fetch_temperatures_for_all_cities(
    db: AsyncSession,
):
    stmt = select(CityModel)
    result = await db.execute(stmt)
    cities = result.scalars().all()

    for city in cities:
        temperature_c = await fetch_temperature_by_city_name(city)

        record = TemperatureModel(
            city_id=city.id,
            date_time=datetime.now(UTC),
            temperature=temperature_c,
        )

        db.add(record)
    await db.commit()


async def get_temperatures(db: AsyncSession) -> List[TemperatureDetailSchema]:
    stmt = select(TemperatureModel)
    result = await db.execute(stmt)
    temperatures = result.scalars().all()
    return [
        TemperatureDetailSchema.model_validate(t)
        for t in temperatures
    ]


async def get_temperatures_by_city_id(
        city_id: int,
        db: AsyncSession
) -> CityDetailSchema:
    stmt = select(CityModel).where(CityModel.id == city_id)
    result = await db.execute(stmt)
    city = result.scalar_one_or_none()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    stmt = select(TemperatureModel).where(TemperatureModel.city_id == city_id)
    result = await db.execute(stmt)
    temperatures = result.scalars().all()

    if not temperatures:
        raise HTTPException(status_code=404, detail=f"{city.name} doesn't have temperatures records.")

    city.temperatures = temperatures

    return CityDetailSchema.model_validate(city)
