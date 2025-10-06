from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from city_temperature.database import get_db
from city_temperature.crud import temperature_crud, city_crud
from city_temperature.schemas import temperature as temperature_schema
from city_temperature.services import temperature_service


router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post("/update", response_model=List[temperature_schema.Temperature])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = city_crud.get_cities(db)
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found in database")

    temperatures = []

    for city in cities:
        temp = await temperature_service.fetch_temperature(city.name)
        if temp is not None:
            temp_data = temperature_schema.TemperatureCreate(
                city_id=city.id, temperature=temp
            )
            new_temp = temperature_crud.create_temperature(db, temp_data)
            temperatures.append(new_temp)

    return temperatures


@router.get("/", response_model=List[temperature_schema.Temperature])
def get_temperatures(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    if city_id:
        temps = temperature_crud.get_temperatures_by_city(db, city_id)
    else:
        temps = temperature_crud.get_all_temperatures(db)
    return temps
