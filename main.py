import asyncio
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal, Base, engine
from services import geocode_city, fetch_current_temperature

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/cities/", response_model=list[schemas.City])
def read_city_list(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@app.get("/cities/{city_id}/", response_model=schemas.City)
def read_single_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="Such city already exists.")
    return crud.create_city(db=db, city=city)


@app.delete("/cities/{city_id}/", status_code=204)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_city(db=db, city_id=city_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="City not found")


@app.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperature_list(city_id: int | None = None, db: Session = Depends(get_db)):
    return crud.get_all_temperatures(db=db, city_id=city_id)


@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_all_cities(db)

    async def fetch_one_city(city):
        coords = await geocode_city(city.name)
        if coords is None:
            return None
        latitude, longitude = coords
        temperature_value = await fetch_current_temperature(latitude, longitude)
        return city, temperature_value

    fetch_results = await asyncio.gather(*(fetch_one_city(city) for city in cities))

    updated = []
    for result in fetch_results:
        if result is None:
            continue
        city, temperature_value = result
        db_temperature = crud.create_temperature(
            db=db,
            temperature=schemas.TemperatureCreate(
                city_id=city.id,
                date_time=datetime.utcnow(),
                temperature=temperature_value,
            ),
        )
        updated.append(db_temperature)

    return updated
