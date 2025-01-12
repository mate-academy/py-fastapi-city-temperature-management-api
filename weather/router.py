from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from weather import schemas, crud

router = APIRouter()


@router.get("/temperatures", response_model=list[schemas.ListWeather])
async def get_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_weather(db=db)


@router.post("/temperatures", response_model=schemas.UpdateWeather)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.update_weather(db=db)


@router.get("/temperatures/{city_id}", response_model=list[schemas.ListWeather])
async def get_temperature(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_one_weather(city_id=city_id, db=db)
