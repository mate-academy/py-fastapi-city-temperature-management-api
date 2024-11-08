from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db
from src.temperature import schemas
from src.temperature import crud

router = APIRouter()


@router.get("/temperature/", response_model=list[schemas.Temperature])
async def get_cities_temperature(city_id: int = None, db: AsyncSession = Depends(get_db)):
    return await crud.list_cities_temperature(db, city_id)


@router.post("/temperature/update/", response_model=list[schemas.Temperature])
async def update_cities_temperature(db: AsyncSession = Depends(get_db)):
    return await crud.set_cities_temperature(db)
