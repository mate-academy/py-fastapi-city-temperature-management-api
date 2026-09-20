import asyncio
import datetime
from typing import List, Optional

import httpx
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import DB

router = APIRouter(
    prefix="/temperatures",
    tags=["temperatures"]
)


async def fetch_temperature_for_city(client: httpx.AsyncClient, city_name: str) -> Optional[float]:
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
        geo_response = await client.get(geo_url, timeout=10.0)
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return None

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = await client.get(weather_url, timeout=10.0)
        weather_data = weather_response.json()

        return weather_data.get("current_weather", {}).get("temperature")
    except Exception:
        return None


@router.post("/update", response_model=List[schemas.Temperature], status_code=status.HTTP_201_CREATED)
async def update_temperatures(db: DB):
    cities = db.query(models.CityDB).all()
    if not cities:
        return []

    new_records = []
    now = datetime.datetime.utcnow()

    async with httpx.AsyncClient() as client:
        tasks = [fetch_temperature_for_city(client, city.name) for city in cities]
        temperatures = await asyncio.gather(*tasks)

        for city, temp in zip(cities, temperatures):
            if temp is not None:
                record = models.TemperatureDB(
                    city_id=city.id,
                    temperature=temp,
                    date_time=now
                )
                db.add(record)
                new_records.append(record)

    db.commit()

    for record in new_records:
        db.refresh(record)

    return new_records


@router.get("/temperatures/", response_model=List[schemas.Temperature])
async def get_all_temperatures(db: DB):
    return db.query(models.TemperatureDB).all()


@router.get("/temperatures/{city_id}", response_model=schemas.Temperature)
async def get_temperatures(city_id: int, db: DB):
    query = db.query(models.TemperatureDB).filter(models.TemperatureDB.city_id == city_id)
    record = query.first()
    if not record:
        return []
    return record.temperature
