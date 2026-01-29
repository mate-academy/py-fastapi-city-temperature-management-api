from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from crud.city import get_cities
from crud.temperature import add_temperature, get_temperatures
from services.weather import fetch_temperature

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update")
async def update(db: AsyncSession = Depends(get_db)):
    cities = await get_cities(db)

    for city in cities:
        lat, lon = map(float, city.additional_info.split(","))

        temp, dt = await fetch_temperature(lat, lon)
        await add_temperature(db, city.id, temp, dt)

    return {"updated": len(cities)}


@router.get("")
async def list_temperatures(
    city_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await get_temperatures(db, city_id)
