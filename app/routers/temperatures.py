from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import httpx
from .. import crud, schemas, database, models

router = APIRouter(
    prefix="/temperatures",
    tags=["temperatures"]
)

@router.post("/update", response_model=List[schemas.TemperatureResponse])
async def update_temperatures(db: Session = Depends(database.get_db)):
    """
    Fetches current temperature for all cities in the DB.
    Optimized to perform a single DB commit after fetching all data.
    """
    cities = crud.get_cities(db, limit=1000)
    
    # List to hold model objects before saving
    new_temperature_records = []
    failed_cities = []
    
    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                # 1. Geocode the city name to get lat/lon
                geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city.name}&count=1&language=en&format=json"
                geo_resp = await client.get(geo_url)
                geo_resp.raise_for_status() # Raise exception for 4xx/5xx errors
                geo_data = geo_resp.json()
                
                if not geo_data.get("results"):
                    print(f"Warning: Could not find coordinates for city: {city.name}")
                    continue
                    
                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]

                # 2. Fetch temperature using lat/lon
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                weather_resp = await client.get(weather_url)
                weather_resp.raise_for_status()
                weather_data = weather_resp.json()
                
                # KeyError handling: Check if API structure is as expected
                current_temp = weather_data["current_weather"]["temperature"]
                
                # Create the model object but DO NOT commit yet
                temp_obj = models.Temperature(city_id=city.id, temperature=current_temp)
                new_temperature_records.append(temp_obj)
                
            except httpx.RequestError as e:
                # Network level errors (DNS, timeout, connection refused)
                print(f"Network error while fetching data for {city.name}: {e}")
                failed_cities.append(city.name)
            except KeyError as e:
                # API response structure changed or data missing
                print(f"Data parsing error for {city.name}: Missing key {e}")
                failed_cities.append(city.name)
            except Exception as e:
                # Catch-all for unexpected errors (e.g. DB connectivity issues during object creation)
                print(f"Unexpected error for {city.name}: {e}")
                failed_cities.append(city.name)

    if not new_temperature_records:
        raise HTTPException(
            status_code=404, 
            detail=f"No weather data updated. Failed cities: {failed_cities}"
        )

    # 3. Batch save to DB (Single Commit)
    saved_records = crud.bulk_create_temperatures(db, new_temperature_records)

    return saved_records

@router.get("/", response_model=List[schemas.TemperatureResponse])
def read_temperatures(
    city_id: Optional[int] = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(database.get_db)
):
    return crud.get_temperatures(db, city_id=city_id, skip=skip, limit=limit)
