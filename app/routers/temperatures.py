from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from ..services import weather
from .. import database, models, schemas, crud

router = APIRouter()

@router.post("/update")
async def update_temperatures(db: AsyncSession = Depends(database.get_db)):
    cities = await crud.get_cities(db)
    for city in cities:
        temp = await weather.get_current_temperature(city.name)
        if temp:
            await crud.create_temperature(db, schemas.TemperatureCreate(temperature=temp), city.id)
    return {"status": "success"}

@router.get("/", response_model=List[schemas.Temperature])
async def read_temperatures(
    city_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_temperatures(db, city_id)
