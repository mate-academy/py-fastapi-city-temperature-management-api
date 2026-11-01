from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import httpx

from app.cities.models import City
from app.db.database import get_db
from app.temperature.models import Temperature
from app.temperature.schemas import TemperatureRead
from app.temperature.services import get_current_temperature

router = APIRouter()

@router.get("", response_model=list[TemperatureRead])
async def get_temperatures(
    city_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Temperature)

    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)

    result = await db.execute(query)
    return result.scalars().all()

@router.post("/update", response_model=list[TemperatureRead])
async def update_temperatures(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(City))
    cities = result.scalars().all()

    async with httpx.AsyncClient(
        base_url="https://api.weatherapi.com",
        timeout=10,
    ) as client:
        values = await asyncio.gather(
            *(
                get_current_temperature(
                    city_name=city.name,
                    client=client,
                )
                for city in cities
            )
        )

    temperatures = [
        Temperature(
            city_id=city.id,
            temperature=value,
        )
        for city, value in zip(cities, values)
    ]

    try:
        db.add_all(temperatures)
        await db.commit()
        return temperatures
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database operation failed",
        )
