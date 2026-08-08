from datetime import datetime
from typing import List, Optional
import httpx
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cities", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="City already registered")
    return crud.create_city(db=db, city=city)


@app.get("/cities", response_model=List[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cities(db, skip=skip, limit=limit)


@app.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.put("/cities/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city: schemas.CityUpdate, db: Session = Depends(get_db)):
    db_city = crud.update_city(db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.delete("/cities/{city_id}", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.delete_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


async def fetch_temperature(client: httpx.AsyncClient, name: str) -> Optional[float]:
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={name}&count=1"
        geo_response = await client.get(geo_url)
        geo_data = geo_response.json()
        if not geo_data.get("results"):
            return None
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = await client.get(weather_url)
        weather_data = weather_response.json()
        return weather_data.get("current_weather", {}).get("temperature")
    except Exception:
        return None


@app.post("/temperatures/update", response_model=List[schemas.Temperature])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)
    recorded_temperatures = []
    now = datetime.utcnow()

    async with httpx.AsyncClient() as client:
        for city in cities:
            temp = await fetch_temperature(client, city.name)
            if temp is not None:
                db_temp = crud.create_temperature(db=db, city_id=city.id, temp=temp, dt=now)
                recorded_temperatures.append(db_temp)

    return recorded_temperatures


@app.get("/temperatures", response_model=List[schemas.Temperature])
def read_temperatures(city_id: Optional[int] = Query(None), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id=city_id, skip=skip, limit=limit)