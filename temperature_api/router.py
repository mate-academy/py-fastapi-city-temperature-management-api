import asyncio
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from city_api.crud import get_temperatures_by_city
from city_api.models import City
from temperature_api.schemas import Temperature, TemperatureCreate
from temperature_api.models import Temperature as TemperatureModel
from temperature_api.weather import get_current_temperature
from dependencies import get_db


temp_router = APIRouter()


@temp_router.post("/temperatures/update", response_model=List[Temperature])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(City).all()
    temperatures_data = []

    async def fetch_temperature(city_name: str):
        try:
            temperature = await get_current_temperature(city_name)
            city = db.query(City).filter(City.name == city_name).first()
            temperature_data = TemperatureCreate(
                city_id=city.id,
                date_time=datetime.utcnow(),
                temperature=temperature
            )
            temperatures_data.append(temperature_data)
        except ValueError as ve:
            print(f"Error fetching temperature data for {city_name}: {ve}")

    tasks = [fetch_temperature(city.name) for city in cities]
    await asyncio.gather(*tasks)

    db_temperatures = [
        TemperatureModel(**data.model_dump()) for data in temperatures_data
    ]
    db.add_all(db_temperatures)
    db.commit()

    for temp in db_temperatures:
        db.refresh(temp)

    return db_temperatures



@temp_router.get("/temperatures", response_model=List[Temperature])
def get_temperature_by_city(
    city_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> List[Temperature]:
    try:
        if city_id is not None:
            temperatures = get_temperatures_by_city(db, city_id, skip, limit)
            if not temperatures:
                raise HTTPException(
                    status_code=404, detail="City not found in the database"
                )
        else:
            temperatures = (
                db.query(TemperatureModel).offset(skip).limit(limit).all()
            )
        return temperatures
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail="Database error occurred"
        ) from e
