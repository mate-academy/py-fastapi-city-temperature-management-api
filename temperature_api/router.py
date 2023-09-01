import asyncio

from city import crud as city_crud
from dependencies import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from temperature_api import schemas, crud, utils

router = APIRouter()


@router.post("/temperatures/update/")
async def create_record(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        cities = await city_crud.get_all_cities(db=db)

        await asyncio.gather(
            *[crud.update_city_temperature(city=city, db=db) for city in cities]
        )

    return {"message": "Temperatures were successfully updated"}


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_city_temperatures(city_id: int = -1, db: AsyncSession = Depends(get_db)):
    return await crud.get_temperatures(id=city_id, db=db)
