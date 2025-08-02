from typing import List, Optional
import random
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from dependencies import get_db
from . import schemas, crud
from city import models as city_models


router = APIRouter()

@router.get("/temperatures", response_model=List[schemas.TemperatureInDB])
async def read_temperatures(
    city_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    if city_id is not None:
        return await crud.get_temperatures_by_city(db, city_id)
    return await crud.get_all_temperatures(db)


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
