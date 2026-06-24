from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.cities.models import City
from app.temperatures.models import Temperature
from app.temperatures.schemas import TemperatureResponse
from app.temperatures.service import fetch_current_temperature


router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post("/update", status_code=status.HTTP_200_OK)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City))
    cities = result.scalars().all()

    if not cities:
        return {"message": "No cities found in database to update."}

    updated_count = 0
    for city in cities:
        temp = await fetch_current_temperature(city.name)
        if temp is not None:
            new_record = Temperature(city_id=city.id, temperature=temp)
            db.add(new_record)
            updated_count += 1

    await db.commit()
    return {"message": f"Successfully updated temperatures for {updated_count} cities."}


@router.get("/", response_model=list[TemperatureResponse])
async def get_temperatures(
        city_id: int | None = Query(None, description="Filter by city ID"),
        db: AsyncSession = Depends(get_db)
):
    query = select(Temperature)
    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)

    result = await db.execute(query)
    return result.scalars().all()
