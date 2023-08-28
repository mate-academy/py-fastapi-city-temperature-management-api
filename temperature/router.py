import asyncio

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import services
from dependencies import get_db
from temperature import schemas, crud
from city import crud as city_crud


router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_all_temperatures(
    db: AsyncSession = Depends(get_db),
        city_id: int = None,
        skip: int = 0,
        limit: int = 10
):
    return await crud.get_temperatures(
        db=db,
        city_id=city_id,
        skip=skip,
        limit=limit
    )


@router.post("/temperatures/update/")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        cities = await city_crud.get_all_cities(db=db)

        await asyncio.gather(
            *[services.update_temperature(city=city, db=db) for city in cities]
        )

    return {"message": "Temperatures were successfully updated"}
