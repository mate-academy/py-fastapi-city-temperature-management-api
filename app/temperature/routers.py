from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.temperature import crud, schemas
from app.city import crud as city_crud
from app.dependencies import get_db
from app.temperature.helpers import fetch_temperature
from datetime import datetime

temperature_router = APIRouter()


@temperature_router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = city_crud.get_cities(db)
    for city in cities:
        temperature = fetch_temperature(city.name)
        if temperature is not None:
            crud.create_temperature(db, schemas.TemperatureCreate(
                city_id=city.id,
                date_time=datetime.utcnow(),
                temperature=temperature
            ))
    return {"ok": True}


@temperature_router.get("/", response_model=list[schemas.TemperatureRead])
def get_temperatures(city_id: int = None, db: Session = Depends(get_db)):
    if city_id is not None:
        temperatures = crud.get_temperatures_by_city_id(db, city_id)
        if not temperatures:
            raise HTTPException(status_code=404, detail="No temperature records found for this city.")
        return temperatures
    return crud.get_temperatures(db)