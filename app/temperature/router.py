import asyncio

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.city.crud import get_all_cities
from app.temperature import crud, schemas
from app.services.temperature_updater import fetch_and_create_temperature


router = APIRouter()


@router.post("/temperatures/update/", response_model=list[schemas.TemperatureRead])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = await asyncio.to_thread(get_all_cities, db=db)

    if not cities:
        raise HTTPException(status_code=404, detail="No cities in database.")

    new_temperatures = await asyncio.gather(
        *(fetch_and_create_temperature(db, city) for city in cities)
    )

    return new_temperatures


@router.get("/temperatures/", response_model=list[schemas.TemperatureRead])
async def get_temperatures(city_id: int | None = Query(default=None), db: Session = Depends(get_db)):

    if city_id is not None:
        temperatures = await asyncio.to_thread(crud.get_temperatures_by_city, db, city_id)
        if not temperatures:
            raise HTTPException(status_code=404, detail=f"No temperatures found for city_id={city_id}")
    else:
        temperatures = await asyncio.to_thread(crud.get_all_temperatures, db)

    return temperatures
