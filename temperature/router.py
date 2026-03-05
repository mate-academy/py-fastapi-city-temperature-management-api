import asyncio
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from dependencies import get_db
from city.crud import get_all_cities
from . import crud, schemas, service

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.get("/", response_model=List[schemas.Temperature])
async def get_all_temperatures(
    city_id: int | None = None, db: AsyncSession = Depends(get_db)
):
    if city_id is None:
        return await crud.get_all_temperatures(db)
    else:
        return await crud.get_temperature_by_city_id(db, city_id)


@router.post("/update", status_code=status.HTTP_201_CREATED)
async def update_temperatures(db: AsyncSession = Depends(get_db)):

    cities = await get_all_cities(db)

    tasks = []
    for city in cities:
        tasks.append(service.get_current_temp_by_name(city.name))

    temperatures = await asyncio.gather(*tasks, return_exceptions=True)

    updated_records = []
    for i, temp in enumerate(temperatures):
        if isinstance(temp, float):
            new_temp_data = schemas.TemperatureCreate(
                city_id=cities[i].id, temperature=temp
            )
            record = await crud.create_temperature(db, new_temp_data)
            updated_records.append(record)

    return {"message": f"Updated {len(updated_records)} records"}
