from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import httpx

from app.database import get_db
from app.models import Temperature as TemperatureModel, City as CityModel
from app.schemas import Temperature, TemperatureCreate

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


async def get_temperature_for_city(city_name: str) -> Optional[float]:
    """
    Fetch current temperature for a city using Open-Meteo API.
    This is a simplified implementation that searches for coordinates.
    In a production environment, you would need a more robust geocoding service.
    """
    try:
        # First, get coordinates for the city using Open-Meteo Geocoding API
        async with httpx.AsyncClient() as client:
            geo_response = await client.get(
                f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
            )
            geo_data = geo_response.json()
            
            if not geo_data.get("results"):
                return None
            
            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]
            
            # Get current temperature
            weather_response = await client.get(
                f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            )
            weather_data = weather_response.json()
            
            return weather_data["current_weather"]["temperature"]
    except Exception as e:
        print(f"Error fetching temperature for {city_name}: {e}")
        return None


@router.post("/update", response_model=List[Temperature], status_code=201)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(CityModel).all()
    
    if not cities:
        raise HTTPException(status_code=400, detail="No cities found in database")
    
    temperatures = []
    
    for city in cities:
        temp = await get_temperature_for_city(city.name)
        
        if temp is not None:
            db_temp = TemperatureModel(
                city_id=city.id,
                temperature=temp,
                date_time=datetime.utcnow()
            )
            db.add(db_temp)
            db.commit()
            db.refresh(db_temp)
            temperatures.append(db_temp)
    
    return temperatures


@router.get("/", response_model=List[Temperature])
def get_temperatures(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(TemperatureModel)
    
    if city_id is not None:
        query = query.filter(TemperatureModel.city_id == city_id)
    
    temperatures = query.order_by(TemperatureModel.date_time.desc()).all()
    return temperatures
