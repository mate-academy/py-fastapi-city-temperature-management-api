from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import crud, schemas


router = APIRouter()


#
@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_cities(
    db: AsyncSession = Depends(get_db), city_id: int | None = None
):
    return await crud.get_all_temperatures(db=db, city_id=city_id)


@router.post("/temperatures/", response_model=schemas.Temperature)
async def create_city(
    temperature: schemas.TemperatureCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_temperature(db=db, temperature=temperature)
