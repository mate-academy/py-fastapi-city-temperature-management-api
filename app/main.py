from datetime import datetime
from typing import List

import requests
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import database, schemas, crud
from app.schemas import CityCreate, TemperatureCreate

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# City API
@app.get("/cities/", response_model=List[schemas.City])
def get_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_cities(db, skip=skip, limit=limit)


@app.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db, city)


@app.get("/cities/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.put("/cities/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city: CityCreate, db: Session = Depends(get_db)):
    db_city = crud.update_city(db=db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.delete("/cities/{city_id}", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.delete_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


# Temperature API
@app.post("/temperatures/update")
async def update_temperature(db: Session = Depends(get_db)):
    cities = crud.get_cities(db=db)
    for city in cities:
        temperature_data = requests.get(f"https://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q={city.name}")
        temp = temperature_data.json().get("current").get("temp_c")
        temperature = TemperatureCreate(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=temp,
        )
        crud.create_temperature(db=db, temperature=temperature)
    return {"message": "Temperature updated successfully"}


@app.get("/temperatures/", response_model=List[schemas.Temperature])
def get_temperatures(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, skip=skip, limit=limit)


@app.get("/temperatures/{city_id}", response_model=List[schemas.Temperature])
def get_temperature(city_id: int, db: Session = Depends(get_db)):
    return crud.get_temperature_by_city(db=db, city_id=city_id)
