from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from temperature import crud
from dependencies import get_async_db, get_db
from temperature import schemas

router = APIRouter()


@router.post("/temperatures/update/")
async def update_temperature(db: AsyncSession = Depends(get_async_db)):
    await crud.set_temperature(db)


@router.get("/temperatures/", response_model=list[schemas.TemperatureListSchema])
def get_temperature(db: Session = Depends(get_db)):
    return crud.get_all_temperature(db)


@router.get("/temperatures/{city_id}/", response_model=list[schemas.TemperatureListSchema])
def get_temperature_for_city(city_id: int, db: Session = Depends(get_db)):
    return crud.get_temperature_for_city(db=db, city_id=city_id)
