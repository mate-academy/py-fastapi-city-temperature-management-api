import asyncio
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from city_crud_api.crud import get_temperatures_by_city

from dependencies import get_db
from models import DBCity
from temperature_api.crud import (
    create_temperature_record,
    update_temperatures_for_cities,
)
from temperature_api.schemas import Temperature
from temperature_api.weather_data import get_current_temperature

router = APIRouter()


@router.post("/temperatures/", response_model=List[Temperature])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(DBCity).all()
    temperatures_data = []

    async def fetch_temperature(city_name: str):
        try:
            temperature = await get_current_temperature(city_name)
            temperature_data = create_temperature_record(db, city_name, temperature)
            temperatures_data.append(temperature_data)
        except ValueError as e:
            print(f"Error fetching temperature data for {city_name}: {e}")

    tasks = [fetch_temperature(city.name) for city in cities]
    await asyncio.gather(*tasks)

    return update_temperatures_for_cities(db, temperatures_data)


@router.get("/temperatures/", response_model=List[Temperature])
def get_temperature_by_city_id(
    city_id: int, db: Session = Depends(get_db)
) -> List[Temperature]:
    try:
        temperatures = get_temperatures_by_city(db, city_id)
        if not temperatures:
            raise HTTPException(
                status_code=404, detail="City not found in the database"
            )
        return temperatures
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred") from e
