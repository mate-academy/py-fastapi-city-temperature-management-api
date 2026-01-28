from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from db.async_session import get_db
from schemas.temperature import Temperature
from crud.utils import fetch_weather
import crud.city as city_crud
import crud.temperature as temp_crud


router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"]
)


@router.get("/", response_model=list[Temperature])
async def read_temperatures(
        city_id: int = Query(None),
        db: AsyncSession = Depends(get_db)
):
    if city_id:
        return await temp_crud.get_temperature_for_city(db, city_id)
    return await temp_crud.get_all_temperature_records(db)


@router.post("/update")
async def update_all_cities_weather(db: AsyncSession = Depends(get_db)):
    cities = await city_crud.get_all_cities(db)

    updated_count = 0
    for city in cities:
        try:
            current_temp = await fetch_weather(city.name)

            await temp_crud.create_temperature_record(
                db, city_id=city.id, temp_value=current_temp
            )
            updated_count += 1
        except Exception as e:
            print(f"Failed to fetch weather for {city.name}: {e}")

    if updated_count > 0:
        await db.commit()

    return {"status": "success", "records_updated": updated_count}
