import asyncio

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city.crud import get_all_cities

from temperature import crud, schemas
from temperature.weather import temperature_for_specific_city

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.list_temperatures(
        db=db,
    )


@router.post("/temperatures/update/")
async def update_temperature(
        db: AsyncSession = Depends(get_db)
):
    cities = await get_all_cities(db=db)
    await asyncio.gather(*[
        temperature_for_specific_city(city=city, db=db)
        for city in cities
    ])

    await db.commit()

    return {"message": "All temperatures successfully updated"}
