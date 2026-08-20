import datetime
import httpx
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import models
from schemas import schemas


router = APIRouter(prefix="/temperatures", tags=["Temperatures"])
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_weather_for_city(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
            geo_response = await client.get(geo_url, timeout=10.0)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            if not geo_data.get("results"):
                raise HTTPException(status_code=404, detail=f"Coordinates for city '{city_name}' not found.")
            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]

            weather_params = {"latitude": lat, "longitude": lon, "current_weather": "true"}
            weather_response = await client.get(WEATHER_API_URL, params=weather_params, timeout=10.0)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            return weather_data["current_weather"]["temperature"]
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"External weather API error: {str(exc)}")


@router.post("/update", status_code=status.HTTP_200_OK)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    if not cities:
        return {"message": "No cities found in database."}
    records_added = 0
    errors = []
    for city in cities:
        try:
            temp_value = await fetch_weather_for_city(city.name)
            temp_record = models.Temperature(city_id=city.id, temperature=temp_value,
                                             date_time=datetime.datetime.utcnow())
            db.add(temp_record)
            records_added += 1
        except Exception as e:
            errors.append({"city": city.name, "error": str(e)})
    db.commit()
    return {"message": f"Successfully updated temperatures for {records_added} cities.", "failed_updates": errors}


@router.get("", response_model=List[schemas.Temperature])
def get_temperatures(city_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    query = db.query(models.Temperature)
    if city_id is not None:
        db_city = db.query(models.City).filter(models.City.id == city_id).first()
        if not db_city:
            raise HTTPException(status_code=404, detail="City not found")
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()
