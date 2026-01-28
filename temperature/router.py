from datetime import datetime, UTC
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from city.models import City
from temperature.crud import get_temperatures
from temperature.models import Temperature
from temperature.schemas import TemperatureRead
from temperature.service import fetch_temperature


router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post("/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = (await db.scalars(select(City))).all()

    for city in cities:
        try:
            temp = await fetch_temperature(city.name)
        except HTTPException:
            continue

        db.add(Temperature(
            city_id=city.id,
            date_time=datetime.now(UTC),
            temperature=temp,
        ))

    await db.commit()
    return {"status": "updated"}


@router.get("", response_model=list[TemperatureRead])
async def list_temperatures(city_id: int | None = None, db: AsyncSession = Depends(get_db)):
    return await get_temperatures(db, city_id)