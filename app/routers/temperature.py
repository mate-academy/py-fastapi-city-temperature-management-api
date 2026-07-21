from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

from app.temperature.models import Temperature
from app.temperature.schemas import TemperatureBaseModel
from app.temperature import crud
from app.dependencies import get_db


router = APIRouter()


@router.get("/temperatures", response_model=list[TemperatureBaseModel])
async def get_all_temperatures(
    db: AsyncSession = Depends(get_db),
    city_id: int | None = None
) -> list[Temperature]:
    return await crud.get_temperature_list(db, city_id)
