from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from .deps import get_db
import httpx
from typing import List

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])

API_KEY = "777972a652d44d4cbd2150547251907"

async def fetch_temperature(client: httpx.AsyncClient, city_name: str) -> float | None:
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": API_KEY,
        "q": city_name,
        "aqi": "no"
    }
    try:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("current", {}).get("temp_c")
    except (httpx.RequestError, httpx.HTTPStatusError):
        return None

@router.post("/update", response_model=List[schemas.TemperatureRead])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)
    results = []
    async with httpx.AsyncClient() as client:
        for city in cities:
            temperature = await fetch_temperature(client, city.name)
            if temperature is not None:
                temp_record = crud.add_temperature(db, city.id, temperature)
                results.append(temp_record)
            else:
                continue
    return results

@router.get("/", response_model=List[schemas.TemperatureRead])
def get_temperatures(city_id: int = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id)
