from typing import List
import random

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime


from dependencies import get_db
from . import models
from . import schemas
from . import crud
from city import models as city_models


router = APIRouter()

@router.get("/temperatures", response_model=List[schemas.TemperatureBase])
async def read_all_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_temperatures(db)


@router.get("/temperatures/", response_model=List[schemas.TemperatureBase])
async def read_temperatures_by_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_temperatures_by_city(db, city_id)


@router.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(city_models.City))
    cities = result.scalars().all()

    for city in cities:
        temp = round(random.uniform(-10.0, 35.0), 1)

        temperature = schemas.TemperatureCreate(
            city_id=city.id,
            date_time=datetime.utcnow(),
            temperature=temp,
        )

        await crud.create_temperature(db, temperature)

    return {"message": "Temperatures got updated."}
