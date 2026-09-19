import logging
import urllib.parse
from datetime import datetime
from typing import List, Optional
import httpx
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
import models
import schemas
import crud

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Weather Analytics Engine Management API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/cities", response_model=schemas.CityResponse, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="City already registered")
    return crud.create_city(db=db, city=city)

@app.get("/cities", response_model=List[schemas.CityResponse])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cities(db, skip=skip, limit=limit)

@app.get("/cities/{city_id}", response_model=schemas.CityResponse)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@app.put("/cities/{city_id}", response_model=schemas.CityResponse)
def update_city(city_id: int, city_update: schemas.CityUpdate, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return crud.update_city(db, db_city=db_city, city_update=city_update)

@app.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    crud.delete_city(db, db_city=db_city)
    return None

@app.post("/temperatures/update", status_code=status.HTTP_200_OK)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db, limit=1000)
    if not cities:
        return {"message": "No cities found in database to update."}

    updated_count = 0
    timestamp = datetime.now()

    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                encoded_name = urllib.parse.quote(city.name)
                geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_name}"
                geo_response = await client.get(geo_url, timeout=10.0)
                geo_response.raise_for_status()
                geo_data = geo_response.json()

                if not geo_data.get("results") or not isinstance(geo_data["results"], list):
                    logger.warning(f"Coordinates not found or invalid format for city: {city.name}")
                    continue
                first_result = geo_data["results"][0]
                lat = first_result.get("latitude")
                lon = first_result.get("longitude")

                if lat is None or lon is None:
                    logger.warning(f"Missing latitude/longitude fields for city: {city.name}")
                    continue

                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                weather_response = await client.get(weather_url, timeout=10.0)
                weather_response.raise_for_status()
                weather_data = weather_response.json()
                current_weather = weather_data.get("current_weather")
                if not current_weather or "temperature" not in current_weather:
                    logger.warning(f"Temperature data missing in API response for city: {city.name}")
                    continue

                current_temp = current_weather["temperature"]
                crud.create_temperature_record(
                    db=db, 
                    city_id=city.id, 
                    temp_value=current_temp, 
                    timestamp=timestamp
                )
                updated_count += 1
                
            except Exception as e:
                logger.error(f"Failed to update temperature for {city.name}: {str(e)}")
                continue

    return {"message": f"Successfully updated temperatures for {updated_count} cities."}

@app.get("/temperatures", response_model=List[schemas.TemperatureResponse])
def read_temperatures(
    city_id: Optional[int] = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return crud.get_temperature_records(db, city_id=city_id, skip=skip, limit=limit)
