import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import get_db
from app import crud, schemas, models
import httpx
import asyncio
import json
from dotenv import load_dotenv
from datetime import datetime

router = APIRouter()

load_dotenv()
API_KEY = os.getenv("API_KEY")
WEATHER_API_URL = os.getenv("WEATHER_API_URL")


async def fetch_temperature_from_weatherapi(city_name: str) -> Optional[dict]:
    params = {
        "key": API_KEY,
        "q": city_name,
        "aqi": "no"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(WEATHER_API_URL, params=params)

        if r.status_code != 200:
            return None

        data = r.json()

        try:
            temp = float(data["current"]["temp_c"])
            lat = float(data["location"]["lat"])
            lon = float(data["location"]["lon"])
            return {
                "temp": temp,
                "lat": lat,
                "lon": lon
            }
        except (json.JSONDecodeError, TypeError, ValueError):
            lat = lon = None


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    if not cities:
        raise HTTPException(status_code=400, detail="No cities found in database")

    async def handle_city(city: models.City):
        result = await fetch_temperature_from_weatherapi(city.name)
        if not result:
            return {"city_id": city.id, "city": city.name, "error": "failed to fetch from WeatherAPI"}

        temp = result["temp"]
        lat = result["lat"]
        lon = result["lon"]

        city.additional_info = json.dumps({"lat": lat, "lon": lon})

        db_temp = crud.create_temperature(
            db, city_id=city.id, temperature_value=temp, date_time=datetime.utcnow()
        )

        return {
            "city_id": city.id,
            "city": city.name,
            "temperature": temp,
            "record_id": db_temp.id
        }

    tasks = [handle_city(c) for c in cities]
    responses = await asyncio.gather(*tasks)

    return {"results": responses}


@router.get("/", response_model=List[schemas.TemperatureRead])
def list_temperatures(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.list_temperatures(db=db, city_id=city_id)
