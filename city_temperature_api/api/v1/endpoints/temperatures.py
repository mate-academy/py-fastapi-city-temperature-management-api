from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from city_temperature_api.database.models.city import City
from city_temperature_api.database.models.temperature import Temperature
from city_temperature_api.database.session.engine import get_db
from city_temperature_api.schemas.temperature import TemperatureResponse
from get_temperature.temperature_utils import get_temperature


router = APIRouter()


@router.get("/", response_model=list[TemperatureResponse])
async def get_temperatures(
        city_id: int = None,
        db: AsyncSession = Depends(get_db)
):
    query = select(Temperature)
    if city_id:
        query = query.where(Temperature.city_id == city_id)

    result = await db.execute(query)
    temperatures = result.scalars().all()

    return temperatures


@router.post("/update", status_code=201)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City))
    cities = result.scalars().all()

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")

    responses = []

    for city in cities:
        temp = await get_temperature(city.name)
        new_temp = Temperature(
            city_id=city.id,
            temperature=temp,
            date_time=datetime.now()
        )

        db.add(new_temp)
        responses.append({"city": city.name, "temperature": temp})

    await db.commit()

    return {"updated_records": responses}
