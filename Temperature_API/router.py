from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, crud
from dependencies import get_db
from .schemas import TemperatureList

router = APIRouter()


# Get all temperature records
@router.get("/temperatures/", response_model=list[schemas.TemperatureList])
async def get_all_temperatures(db: AsyncSession = Depends(get_db)):
    """
    Get a list of all temperature records.
    """
    return await crud.get_all_temperatures(db=db)


# Get temperatures for city by id
@router.get(
    "/temperatures/{city_id}/",
    response_model=TemperatureList
)
async def get_temperatures_by_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Get temperature records for a specific city.
    """
    temperatures = await crud.get_temperature_by_city(db=db, city_id=city_id)
    if not temperatures:
        raise HTTPException(
            status_code=404,
            detail="No temperatures found for this city."
        )
    return temperatures


@router.post("/temperatures/update", response_model=dict)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    """
       Update temperatures for all cities from the weather API.
    """
    return await crud.update_temperatures(db=db)
