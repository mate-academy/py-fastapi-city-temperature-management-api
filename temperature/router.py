from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db, common_parameters
from . import crud, schemas

router = APIRouter()


@router.post("/temperatures/update/", response_model=schemas.Temperature)
async def create_temperature(
        data: schemas.TemperatureCreate, db: AsyncSession = Depends(get_db)
) -> dict:
    """Fetch the current temperature for all cities in the DB from https://www.weatherapi.com/ & store in DB"""
    response = await crud.save_temperature(temperature_data=data, db=db)
    return response


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
        commons: Annotated[dict, Depends(common_parameters)],
        city_id: int = None,
        date: str = None,
        db: AsyncSession = Depends(get_db),

) -> list[schemas.Temperature]:
    if city_id:
        result = await crud.get_temperature_by_city_id(city_id=city_id, db=db)
        return result
    if date:
        result = await crud.get_temperature_by_date(date=date, db=db)
        return result
    return await crud.get_temperatures(db=db, **commons)
