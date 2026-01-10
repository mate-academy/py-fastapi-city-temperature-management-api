from datetime import datetime
from typing import Any, Generator, Union

import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import inspect
from sqlalchemy.orm import Session

import schemas
from db import models
from db.engine import engine, SessionLocal
from db.models import Base
import crud


app = FastAPI()

def get_db() -> Generator[Any, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base.metadata.create_all(bind=engine)

@app.get("/check-db/")
def check_db():
    # Отримуємо список усіх таблиць, які реально існують у файлі
    tables = inspect(engine).get_table_names()
    return {"tables": tables}


@app.get("/")
def read_root() -> dict:
    return {"Hello": "Mate"}


@app.get("/cities/", response_model=list[schemas.City])
def get_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@app.post("/cities/", response_model=schemas.City)
def create_city_one(
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
):
    db_city = crud.get_city_by_name(db, city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="City already exists")

    return crud.create_city(db=db, city=city)


@app.get("/cities/{city_id}/", response_model=schemas.City)
def get_city_by_id_from_db(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return crud.get_city_by_id(db=db, city_id=city_id)

@app.put("/cities/{city_id}/", response_model=schemas.City)
def update_city_endpoint(
        city_id: int,
        city_data: schemas.CityUpdate,
        db: Session = Depends(get_db)
):
    # Викликаємо функцію з crud.py
    updated_city = crud.update_city(db, city_id=city_id, city_update=city_data)

    if updated_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return updated_city


@app.delete("/cities/{city_id}/")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.delete_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": f"City {db_city.name} with id {city_id} deleted successfully"}


@app.post("/temperatures/update")
async def update_all_temperatures(db: Session = Depends(get_db)):
    # 1. Отримуємо всі міста з бази
    cities = db.query(models.DBCity).all()
    if not cities:
        raise HTTPException(
            status_code=404,
            detail="No cities found in database. Please add a city first."
        )

    async with httpx.AsyncClient() as client:
        for city in cities:
            # 2. Запитуємо координати або погоду за назвою міста
            # Для простоти використаємо Open-Meteo Geocoding + Weather API
            try:
                # Отримуємо координати міста за його назвою
                geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city.name}&count=1&language=en&format=json"
                geo_res = await client.get(geo_url)
                geo_data = geo_res.json()

                if not geo_data.get("results"):
                    print(f"Coordinates not found for {city.name}")
                    continue

                location = geo_data["results"][0]
                lat, lon = location["latitude"], location["longitude"]

                # Отримуємо поточну температуру
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                weather_res = await client.get(weather_url)
                temp = weather_res.json()["current_weather"]["temperature"]

                # 3. Зберігаємо в таблицю DBTemperature
                crud.create_temperature(db, city_id=city.id, temperature=temp)

            except Exception as e:
                print(f"Error fetching for {city.name}: {e}")
                continue

    return {"status": "success", "message": f"Updated temperatures for {len(cities)} cities"}


@app.get("/temperatures/", response_model=list[schemas.Temperature])
def get_temperatures(db: Session = Depends(get_db)):
    temperatures = db.query(models.DBTemperature).all()
    if not temperatures:
        raise HTTPException(status_code=404, detail="No temperatures found")
    return temperatures


@app.get("/temperatures/", response_model=Union[schemas.Temperature, list[schemas.Temperature]])
def get_temperature_by_city_id(city_id: int, db: Session = Depends(get_db)):

    db_city = crud.get_city_by_id(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    temperatures = crud.get_temperatures_for_special_city(db=db, city_id=city_id)
    if not temperatures:
        raise HTTPException(status_code=404, detail="Temperatures not found")
    return temperatures
