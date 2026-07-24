import asyncio
from datetime import datetime
from typing import List, Optional
import httpx
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import City, Temperature
from app.schemas import TemperatureResponse, TemperatureUpdateSummary
from app.services import fetch_temperature_for_city

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post("/update", response_model=TemperatureUpdateSummary, status_code=status.HTTP_200_OK)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City))
    cities = result.scalars().all()

    if not cities:
        return TemperatureUpdateSummary(updated_count=0, failed_cities=[])

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_temperature_for_city(client, city.name) for city in cities]
        results = await asyncio.gather(*tasks)

    now = datetime.utcnow()
    records_to_add = []
    failed_cities = []

    for city, temp in zip(cities, results):
        if temp is not None:
            records_to_add.append(Temperature(city_id=city.id, date_time=now, temperature=temp))
        else:
            failed_cities.append(city.name)

    if records_to_add:
        db.add_all(records_to_add)
        await db.commit()

    return TemperatureUpdateSummary(
        updated_count=len(records_to_add),
        failed_cities=failed_cities
    )


@router.get("", response_model=List[TemperatureResponse])
async def get_temperatures(
    city_id: Optional[int] = Query(None, description="Filter temperature logs by city ID"),
    db: AsyncSession = Depends(get_db)
):
    query = select(Temperature)
    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)

    result = await db.execute(query)
    return result.scalars().all()
