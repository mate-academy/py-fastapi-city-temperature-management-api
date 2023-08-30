import asyncio

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import schemas
from city.crud import get_all_cities
from dependencies import get_db
from temperature.crud import get_all_temperatures
from temperature.services import update_temperature

router = APIRouter()


@router.post("/temperatures/update/")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        cities = await get_all_cities(db=db)

        await asyncio.gather(*[update_temperature(city=city, db=db) for city in cities])

    return {"message": "Temperatures were successfully updated"}


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def temperature_get(city_id: int = None, db: AsyncSession = Depends(get_db)):
    return await get_all_temperatures(db=db, city_id=city_id)
