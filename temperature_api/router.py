from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature_api import schemas, crud

router = APIRouter()


@router.post("/temperatures/update", response_model=list[schemas.TemperatureCreate])
async def update_temperature_route(db: AsyncSession = Depends(get_db)):
    updated_temperatures = await crud.update_temperature(db)
    return updated_temperatures


@router.get("/temperatures/", response_model=schemas.TemperatureList)
async def get_temperature_route(db: AsyncSession = Depends(get_db)):
    temperatures = await crud.get_temperature(db)
    if not temperatures:
        raise HTTPException(status_code=404, detail="No temperature records found.")
    return {"temperature_list": temperatures}


@router.get("/temperatures/{city_id}", response_model=schemas.TemperatureRead)
async def get_temperature_route(city_id: int, db: AsyncSession = Depends(get_db)):
    city_temperature = await crud.get_temperature_by_city_id(city_id=city_id, db=db)
    if not city_temperature:
        raise HTTPException(status_code=404, detail=f"No temperature records found for city ID {city_id}.")
    return city_temperature
