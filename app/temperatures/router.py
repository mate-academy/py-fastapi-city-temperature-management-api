from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.temperatures.schemas import Temperature
from app.temperatures import service

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post(
    "/update", response_model=list[Temperature], status_code=status.HTTP_200_OK
)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    return await service.fetch_and_update_temperatures(db)


@router.get("/", response_model=list[Temperature])
async def get_temperatures(
    city_id: int | None = Query(
        default=None, description="Filter temperature records by city ID"
    ),
    db: AsyncSession = Depends(get_db),
):
    return await service.get_all_temperatures(db, city_id=city_id)
