from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from deps import get_session
from models import City, Temperature
from schemas import TemperatureResponse
from services.weather import fetch_temperature

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post("/update")
async def update_temperatures(session: AsyncSession = Depends(get_session)):
    cities = (await session.execute(select(City))).scalars().all()

    for city in cities:
        try:
            temp = await fetch_temperature(city.name)
            session.add(Temperature(city_id=city.id, temperature=temp))
        except Exception as e:
            # Можна логувати або просто ігнорувати
            print(f"Failed to fetch temperature for {city.name}: {e}")

    await session.commit()
    return {"status": "ok"}


@router.get("", response_model=List[TemperatureResponse])
async def list_temperatures(
    city_id: Optional[int] = None,
    session: AsyncSession = Depends(get_session),
):
    stmt = select(Temperature)
    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)

    result = await session.execute(stmt)
    return result.scalars().all()
