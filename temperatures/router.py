from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cities.crud import get_all_cities
from database import get_db
from temperatures import schemas, crud, service

router = APIRouter()


@router.get("/", response_model=List[schemas.TemperatureRead])
async def get_temperatures(db: AsyncSession = Depends(get_db), city_id: int = None):
    return await crud.get_all_temperatures(db, city_id)


@router.post("/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await get_all_cities(db)
    records_added = 0

    for city in cities:
        try:
            current_temp = await service.get_current_temp(
                city.latitude,
                city.longitude
            )
            await crud.create_temperature_record(db, city.id, current_temp)
            records_added += 1
        except Exception as e:
            print(f"Error updating {city.name}: {e}")

    return {"message": f"Updated records for {records_added} cities."}
