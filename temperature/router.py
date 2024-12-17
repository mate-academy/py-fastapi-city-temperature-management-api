from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import get_cities, get_city_by_id
from dependencies import get_db
from temperature import crud, models, schemas


router = APIRouter()


@router.post(
    "/temperatures/update",
    response_model=schemas.TemperatureUpdateResponse
)
async def update_temperatures(db: AsyncSession = Depends(get_db)):

    cities = await get_cities(db=db, limit=None)

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found in the database.")

    temperatures = []

    for city in cities:
        try:
            temperature = await crud.fetch_temperature(city.name)
            new_temperature = models.DBTemperature(
                city_id=city.id,
                date_time=datetime.utcnow(),
                temperature=temperature
            )
            db.add(new_temperature)
            temperatures.append(schemas.TemperatureCreate(
                city_id=city.id,
                city=city.name,
                date_time=new_temperature.date_time,
                temperature=new_temperature.temperature
            ))
        except HTTPException as e:
            raise e.detail

    await db.commit()

    return schemas.TemperatureUpdateResponse(
        message="Temperatures updated successfully",
        updated_records=len(temperatures),
        temperatures=temperatures
    )


@router.get("/temperatures", response_model=List[schemas.Temperature])
async def list_temperatures(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_temperatures(db, skip=skip, limit=limit)


@router.get(
    "/temperatures/{city_id}/",
    response_model=schemas.TemperatureResultsResponse
)
async def read_temperatures_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    db_temps = await crud.get_temperature_by_city_id(db=db, city_id=city_id)

    temps = []
    if not db_temps:
        raise HTTPException(status_code=404, detail="City not found")

    city = await get_city_by_id(db=db, city_id=city_id)

    for db_temp in db_temps:
        temps.append(schemas.TemperatureResults(
            id=db_temp.id,
            city_id=db_temp.city_id,
            date_time=db_temp.date_time,
            temperature=db_temp.temperature
            ))

    return schemas.TemperatureResultsResponse(
        message="Temperatures got successfully",
        city=city.name,
        temperatures=temps
    )
