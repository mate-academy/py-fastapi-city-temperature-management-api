from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import get_db
import httpx
import asyncio

router = APIRouter(prefix="/temperatures", tags=["temperatures"])

async def geocode_city(name: str) -> tuple:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": name, "count": 1, "language": "en", "format": "json"}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results") or []
        if not results:
            return (None, None)
        first = results[0]
        return (first.get("latitude"), first.get("longitude"))

async def fetch_temperature_for_coords(lat: float, lon: float) -> float:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "current_weather": "true"}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data.get("current_weather", {}).get("temperature")

async def fetch_temperature(city):
    if city.latitude is not None and city.longitude is not None:
        lat, lon = city.latitude, city.longitude
    else:
        lat, lon = await geocode_city(city.name)
    if lat is None or lon is None:
        return None
    temp = await fetch_temperature_for_coords(lat, lon)
    return temp

@router.post("/update", response_model=list[schemas.Temperature])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    if not cities:
        raise HTTPException(status_code=404, detail="No cities available")
    tasks = [fetch_temperature(city) for city in cities]
    temps = await asyncio.gather(*tasks)
    result = []
    for city, temp in zip(cities, temps):
        if temp is None:
            continue
        record = crud.create_temperature(db, city.id, temp)
        result.append(record)
    return result

@router.get("/", response_model=list[schemas.Temperature])
def list_temperatures(city_id: int = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id)
