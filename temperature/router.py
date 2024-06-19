from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import crud, schemas, utils
from city import crud as city_crud

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_temperatures(db=db)


@router.get("/temperatures/{city_id}/", response_model=schemas.Temperature)
async def read_temperatures_by_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_temperature(db=db, city_id=city_id)


@router.post("/temperatures/update/")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await city_crud.get_all_cities(db=db)
    temperature_data = await utils.fetch_temperature_data(cities)
    now = datetime.now()
    temperatures = [
        schemas.TemperatureCreate(
            date_time=now,
            temperature=temp,
            city_id=city_id
        )
        for city_id, temp in temperature_data.items()
    ]
    await crud.create_temperatures(db=db, temperatures=temperatures)
    return {"message": "Temperatures are loaded"}
