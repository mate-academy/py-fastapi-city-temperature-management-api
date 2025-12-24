import asyncio

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import City, Temperature

from database import get_db
from temperature.schemas import TemperatureOut
from temperature.crud import get_cities_temperature_or_by_city_id, fetch_temperature

router = APIRouter()


@router.post("/update/")
async def update_temperature(
        db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(City))
    cities = result.scalars().all()

    async def process_city(city: City):
        temp = await fetch_temperature(city.name)
        if temp is not None:
            db.add(
                Temperature(
                    city_id=city.id,
                    temperature=temp
                )
            )
            return {"city": city.name, "temp": temp}
    tasks = [process_city(city) for city in cities]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    updated = []
    for r in results:
        if isinstance(r, Exception):
            print(f"Error fetching temperature: {r}")
        elif r is not None:
            db.add(Temperature(city_id=r["city_id"], temperature=r["temp"]))
            updated.append({"city": r["city_name"], "temp": r["temp"]})
    await db.commit()
    return {"updated": updated}


@router.get("/",
            response_model=list[TemperatureOut],
            summary="return all cities with temperature or temperature of one city by id",
            status_code=status.HTTP_200_OK)
async def get_temperature(city_id: int | None = None, db: AsyncSession = Depends(get_db)):
    return await get_cities_temperature_or_by_city_id(city_id=city_id, db=db)



