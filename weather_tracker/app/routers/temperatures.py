from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import httpx
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])

async def fetch_weather(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        geo_response = await client.get(geo_url)
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            raise HTTPException(status_code=404, detail=f"Coordinates for city '{city_name}' not found")
            
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = await client.get(weather_url)
        weather_data = weather_response.json()
        
        return weather_data["current_weather"]["temperature"]


@router.post("/update", status_code=200)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.city.get_multi(db)
    if not cities:
        return {"message": "No cities in database to update."}

    updated_count = 0
    errors = []

    for city in cities:
        try:
            temp = await fetch_weather(city.name)

            crud.temperature.create_record(db, city_id=city.id, temp=temp)
            updated_count += 1
        except Exception as e:
            errors.append(f"Could not update {city.name}: {str(e)}")

    return {
        "message": f"Successfully updated temperatures for {updated_count} cities.",
        "errors": errors
    }


@router.get("/", response_model=List[schemas.TemperatureResponse])
def read_temperatures(
    city_id: Optional[int] = Query(None, description="Filter by City ID"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.temperature.get_multi_by_city(db, city_id=city_id, skip=skip, limit=limit)
