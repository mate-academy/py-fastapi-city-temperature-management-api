from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from crud.city import get_cities
from crud.temperature import get_temperatures
from services.weather import fetch_temperature
from models.temperature import Temperature

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update")
async def update(db: AsyncSession = Depends(get_db)):
    cities = await get_cities(db)
    new_records = []

    for city in cities:
        try:
            lat, lon = map(float, city.additional_info.split(","))
        except (AttributeError, ValueError, TypeError):
            print(f"Skipping city {city.name}: invalid additional_info")
            continue

        temp, dt = await fetch_temperature(lat, lon)
        if temp is None:
            print(f"Skipping city {city.name}: weather API failed")
            continue

        new_records.append(Temperature(city_id=city.id, temperature=temp, date_time=dt))

    for record in new_records:
        db.add(record)
    await db.commit()

    return {"updated": len(new_records)}


@router.get("")
async def list_temperatures(
    city_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await get_temperatures(db, city_id)
