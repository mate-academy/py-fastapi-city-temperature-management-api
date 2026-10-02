from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models import City, Temperature
from app.schemas import TemperatureResponse, TemperatureUpdateResponse
from app.services import update_temperatures_for_cities

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post(
    "/update",
    response_model=TemperatureUpdateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City))
    cities = result.scalars().all()

    new_records = await update_temperatures_for_cities(cities, db)
    return TemperatureUpdateResponse(
        updated_count=len(new_records), records=new_records
    )


@router.get("/", response_model=List[TemperatureResponse])
async def get_temperatures(
    city_id: Optional[int] = Query(
        None, description="Необов'язковий ID міста для фільтрації"
    ),
    db: AsyncSession = Depends(get_db),
):
    query = select(Temperature)
    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)

    query = query.order_by(Temperature.date_time.desc())
    result = await db.execute(query)
    return result.scalars().all()
