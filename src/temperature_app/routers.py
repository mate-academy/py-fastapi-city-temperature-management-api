from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.temperature_app import crud, schemas
from src.utils import get_db

temp_router = APIRouter(prefix="/temperatures", tags=["Temperature"])

@temp_router.post("/update/", response_model=list[schemas.Temperature])
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.update_cities_temperature(db)

@temp_router.get("/", response_model=list[schemas.Temperature])
async def list_temperatures(
    city_id: int = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_temperatures(db, city_id, skip, limit)