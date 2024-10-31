from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from src.dependencies import get_db
from src.temperature import crud
from src.temperature.schemas import Temperature as TemperatureSchema
from src.temperature.temperature_fetcher import fetch_and_update_temperatures

router = APIRouter()


@router.post("/temperatures/update/")
async def update_temperatures(
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    background_tasks.add_task(fetch_and_update_temperatures, db)
    return {"message": "Temperature update initiated in the background"}


@router.get("/temperatures/", response_model=List[TemperatureSchema])
async def get_temperatures_endpoint(
        city_id: Optional[int] = None,
        db: AsyncSession = Depends(get_db),
) -> List[TemperatureSchema]:
    return await crud.get_temperatures(db, city_id=city_id)
