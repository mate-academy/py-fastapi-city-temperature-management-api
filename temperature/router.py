from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db, pagination_parameters
from . import schemas, crud
from city.crud import get_all_cities
from .utils import get_temperature_data
import asyncio

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.TemperatureRead])
async def read_temperatures(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(pagination_parameters),
):
    try:
        temperatures = await crud.get_all_temperatures(
            db=db, skip=pagination["skip"], limit=pagination["limit"]
        )
        return temperatures
    except Exception:
        raise HTTPException(status_code=500, detail="Помилка при отриманні температур")


@router.get("/temperatures/{city_id}", response_model=list[schemas.TemperatureRead])
async def get_temperature_for_city(
    city_id: int,
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(pagination_parameters),
):
    try:
        temperatures = await crud.get_temperatures_by_city(
            db=db, city_id=city_id, skip=pagination["skip"], limit=pagination["limit"]
        )
        if not temperatures:
            raise HTTPException(status_code=404, detail="Немає даних для цього міста")
        return temperatures
    except HTTPException as he:
        raise he
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=f"Помилка при отриманні температури для міста з id={city_id}",
        )


@router.post("/temperatures/update", response_model=list[schemas.TemperatureRead])
async def fetch_temperatures(db: AsyncSession = Depends(get_db)):
    try:
        cities = await get_all_cities(db)
    except Exception:
        raise HTTPException(status_code=500, detail="Помилка при отриманні списку міст")

    try:
        tasks = [get_temperature_data(city=city) for city in cities]
        results = await asyncio.gather(*tasks)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Помилка при зборі даних про температуру"
        )

    valid_results = [schemas.TemperatureCreate(**res) for res in results if res]

    try:
        created_temperatures = await crud.bulk_create_temperatures(db, valid_results)
        return created_temperatures
    except Exception:
        raise HTTPException(
            status_code=500, detail="Помилка при збереженні температур у базу даних"
        )
