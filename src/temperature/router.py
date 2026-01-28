from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db
from src.temperature import crud, service
from src.temperature.schemas import TemperatureRead

router = APIRouter()


@router.post("/temperatures/update")
async def update_weather_data(db: Annotated[AsyncSession, Depends(get_db)]):
    return await service.update_temperatures(db)


@router.get("/temperatures", response_model=List[TemperatureRead])
async def get_temperatures(
        db: Annotated[AsyncSession, Depends(get_db)],
        city_id: Optional[int] = None
):
    return await crud.get_temperatures(db, city_id=city_id)
