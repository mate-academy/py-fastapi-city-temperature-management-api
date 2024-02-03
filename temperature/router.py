from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import crud, schemas
from temperature.fetching_temp_time import fetch_current_temperature_and_time_for_cities

router = APIRouter()


@router.get("/temperatures/list/", response_model=list[schemas.Temperature])
async def get_all_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_temperatures(db=db)


@router.post("/temperatures/update/")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    city_temp_info = await fetch_current_temperature_and_time_for_cities(db=db)

    return await crud.create_or_update_temperatures(
        db=db, city_temp_info=city_temp_info
    )


@router.get("/temperatures/", response_model=schemas.Temperature)
async def get_specific_temperature_by_city_id(
    city_id: int = Query(title="city_id", description="Id for specific city"),
    db: AsyncSession = Depends(get_db),
):
    return await crud.get_temperature_for_specific_city(db=db, city_id=city_id)
