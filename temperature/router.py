from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import crud, schemas
from temperature.weather import get_weather_temperatures


router = APIRouter()


@router.post("/temperatures/update/")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    temperature_records = await get_weather_temperatures(db=db)
    return await crud.create_temperature_records(
        db=db,
        temperature_records=temperature_records
    )


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.get_temperature_list(db=db)


@router.get("/temperatures/{city_id}", response_model=list[schemas.Temperature])
async def get_temperature(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_temperature(db=db, city_id=city_id)

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city
