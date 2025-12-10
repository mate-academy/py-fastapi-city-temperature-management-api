from datetime import datetime

import httpx
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI(title="City Temperature Management API")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/cities/", response_model=List[schemas.City])
def read_cities(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return crud.get_cities(db, skip=skip, limit=limit)


@app.post("/cities/", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
):
    db_city = crud.get_city_by_name(db, name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="City already exists")

    return crud.create_city(db=db, city=city)


@app.get("/cities/{city_id}/", response_model=schemas.City)
def read_single_city(
        city_id: int,
        db: Session = Depends(get_db)
):
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@app.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(
        city_id: int,
        city: schemas.CityUpdate,
        db: Session = Depends(get_db)
):
    db_city = crud.update_city(db=db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@app.delete("/cities/{city_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(
        city_id: int,
        db: Session = Depends(get_db)
):
    db_city = crud.delete_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return None


@app.get("/temperatures/", response_model=List[schemas.Temperature])
def read_temperatures(
        city_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    if city_id:
        return crud.get_temperatures_by_city(db=db, city_id=city_id, skip=skip, limit=limit)

    return crud.get_temperatures(db=db, skip=skip, limit=limit)


@app.post("/temperatures/update/", response_model=List[schemas.Temperature])
async def update_temperatures(db: Session = Depends(get_db), date_time: datetime.datetime = Depends(datetime.datetime.utcnow)):
    cities = crud.get_cities(db, limit=1000)
    new_temperatures = []

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found in database to update")

    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                geo_url = "https://geocoding-api.open-meteo.com/v1/search"
                geo_params = {"name": city.name, "count": 1, "language": "en", "format": "json"}

                geo_resp = await client.get(geo_url, params=geo_params)
                geo_data = geo_resp.json()

                if not geo_data.get("results"):
                    print(f"Skipping {city.name}: Coordinates not found.")
                    continue

                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]

                weather_url = "https://api.open-meteo.com/v1/forecast"
                weather_params = {
                    "latitude": lat,
                    "longitude": lon,
                    "current_weather": "true"
                }

                weather_resp = await client.get(weather_url, params=weather_params)
                weather_data = weather_resp.json()

                current_temp = weather_data.get("current_weather", {}).get("temperature")

                if current_temp is None:
                    continue

                temp_data = schemas.TemperatureCreate(
                    city_id=city.id,
                    temperature=float(current_temp),
                    date_time=date_time
                )

                new_temp = crud.create_temperature(db=db, temperature=temp_data)
                new_temperatures.append(new_temp)

            except Exception as e:
                print(f"Error updating city {city.name}: {e}")
                continue

    return new_temperatures
