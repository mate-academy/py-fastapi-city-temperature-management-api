from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import temperature.crud as crud
import temperature.schemas as schemas
import temperature.utils as utils
from dependencies import get_db
from temperature.models import TemperatureModel

router = APIRouter()


@router.post("/temperatures/update/", response_model=Dict[str, str])
async def update_temperatures(db: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    cities = await utils.get_cities_id_and_name(db)
    for city_id, city_name in cities:
        data = await utils.fetch_weather(city_name)
        temperature = TemperatureModel(city_id=city_id, temperature=data["temperature"])
        db.add(temperature)

    await db.commit()

    return {"msg": "Temperatures was successfully changed."}


@router.get("/temperatures/{city_id}", response_model=schemas.TemperatureListResponse)
async def get_temperature_by_city(
    city_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.TemperatureListResponse:
    results = await crud.get_temperature_by_city(db, city_id)
    if len(results) == 0:
        raise HTTPException(status_code=404, detail="City was not found")
    return schemas.TemperatureListResponse(temperatures=results)


@router.get("/temperatures/", response_model=schemas.TemperatureListResponse)
async def get_temperatures(
    db: AsyncSession = Depends(get_db),
) -> schemas.TemperatureListResponse:
    results = await crud.get_temperatures(db)
    return schemas.TemperatureListResponse(temperatures=results)
