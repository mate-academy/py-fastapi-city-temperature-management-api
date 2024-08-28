from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.temperature import schemas, crud_temperature
from database import get_db
router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
    city_id: int = None,
    db: AsyncSession = Depends(get_db)
) -> list[schemas.Temperature]:
    temperatures = await crud_temperature.get_temperature(db, city_id)
    return temperatures


@router.post("/temperatures/", response_model=schemas.Temperature)
async def create_temperature(
    temperature: schemas.TemperatureCreate,
    db: AsyncSession = Depends(get_db)
) -> schemas.Temperature:
    return await crud_temperature.create_temperature(db, temperature)
