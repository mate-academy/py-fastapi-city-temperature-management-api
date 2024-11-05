from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from . import models, schemas, crud
from dependencies import get_db

router = APIRouter()


@router.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    # Get all cities from the database
    result = await db.execute(select(models.City))
    cities = result.scalars().all()

    temperatures_data = []

    # Fetch and store temperature for each city
    for city in cities:
        try:
            temperature = await crud.fetch_current_temperature(city.name)
            temperatures_data.append({
                "city_id": city.id,
                "date_time": datetime.now(),
                "temperature": temperature
            })
        except Exception as e:
            continue  # Skip if fetching temperature fails

    # Store temperature data in the database
    await crud.fetch_and_store_temperatures(db, temperatures_data)
    return {"detail": "Temperatures updated successfully"}


@router.get("/temperatures", response_model=list[schemas.TemperatureRead])
async def get_all_temperatures(db: AsyncSession = Depends(get_db)):
    temperatures = await crud.get_temperatures(db)
    return [schemas.TemperatureRead.from_orm(temp) for temp in temperatures]


@router.get("/temperatures/", response_model=list[schemas.TemperatureRead])
async def get_temperatures_by_city(city_id: int, db: AsyncSession = Depends(get_db)):
    temperatures = await crud.get_temperature_by_city_id(db, city_id)
    if not temperatures:
        raise HTTPException(status_code=404, detail="No temperature records found for this city")
    return [schemas.TemperatureRead.from_orm(temp) for temp in temperatures]
