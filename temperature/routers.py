from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from temperature import crud, schemas
from dependencies import get_db

router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"],
)


@router.post("/update", response_model=list[schemas.TemperatureList])
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.update_all_temperatures(db)


@router.get("/", response_model=list[schemas.TemperatureList])
async def read_temperatures(city_id: int | None = None, db: AsyncSession = Depends(get_db)):
    if city_id:
        return await crud.get_temperatures_by_city(db, city_id)
    return await crud.get_all_temperatures(db)
