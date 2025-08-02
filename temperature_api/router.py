from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from city_crud_api.crud import crud_update_city
from city_crud_api.schemas import CityUpdate
from database import get_async_db
from dependencies import get_db
from models.city_models import City
from models.temperature_models import Temperature
from temperature_api.crud import (
    fetch_temperature,
    get_temperature_by_city_id_crud,
    get_temperatures_crud,
)
from temperature_api.schemas import TemperatureBase


temperature_router = APIRouter()

@temperature_router.get("/temperatures/", response_model=list[TemperatureBase])
def list_temperatures(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return get_temperatures_crud(db=db, skip=skip, limit=limit)

@temperature_router.get("/temperatures/{city_id}", response_model=TemperatureBase)
def get_temperature_city_by_id(
    city_id: int,
    db: Session = Depends(get_db)
):
    db_city_temperature = get_temperature_by_city_id_crud(db=db, city_id=city_id)
    if db_city_temperature is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city_temperature


@temperature_router.put("/cities/{city_id}", response_model=TemperatureBase)
async def update_city(
        city_id: int,
        city: CityUpdate,
        db: AsyncSession = Depends(get_async_db)
):
    db_city = await crud_update_city(db=db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@temperature_router.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(City))
    cities = result.scalars().all()

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found.")

    for city in cities:
        try:
            temp_c = await fetch_temperature(city.name)
            temperature = Temperature(
                city_id=city.id,
                date_time=datetime.utcnow(),
                temperature=temp_c
            )
            db.add(temperature)
        except Exception as e:
            print(f"Error updating temperature for {city.name}: {e}")

    await db.commit()
    return {"detail": f"Updated temperatures for {len(cities)} cities."}

@temperature_router.get("/debug-session")
async def debug_session(db: AsyncSession = Depends(get_async_db)):
    print("TYPE OF DB:", type(db))
    return {"type": str(type(db))}

