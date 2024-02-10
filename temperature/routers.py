
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession


from temperature import schemas, crud
from temperature.weather import get_temperature_request
from dependencies import get_db

router = APIRouter()


@router.get("/update_temperatures/")
async def update_cities_temperature(
        db: AsyncSession = Depends(get_db)
) -> dict:
    info = await get_temperature_request(db=db)

    return await crud.update_cities_temperature(db=db, info=info)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_temperatures(
        db: AsyncSession = Depends(get_db)
) -> list[schemas.Temperature]:
    return await crud.get_all_temperatures(db=db)


@router.get("/temperatures/{city_id}/", response_model=schemas.TemperatureCity)
async def get_temperature_by_city_id(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> schemas.TemperatureCity | HTTPException:
    db_temperature = await crud.get_temperature_by_city_id(db=db, city_id=city_id)

    if db_temperature is None:
        return HTTPException(status_code=404, detail="City not found")

    return db_temperature
