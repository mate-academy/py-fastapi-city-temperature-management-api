from datetime import datetime, timezone
from typing import List, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db

router = APIRouter(prefix="/temperatures", tags=["temperatures"])

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"  # current=temp_2m


async def _fetch_city_temperature(
        client: httpx.AsyncClient,
        city: models.City
) -> Optional[float]:
    """Resolve city name to lat/lon, then fetch current temperature in °C.
    Returns None if the city can't be resolved.
    """
    try:
        # 1) geocode
        resp = await client.get(
            GEOCODING_URL,
            params={"name": city.name, "count": 1}
        )
        resp.raise_for_status()
        data = resp.json()
        if not data or not data.get("results") or len(data["results"]) == 0:
            return None
        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]
        # 2) weather
        w = await client.get(WEATHER_URL, params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m",
            "timezone": "UTC",
        })
        w.raise_for_status()
        wd = w.json()
        # Open-Meteo 'current' block (new API)
        # OR 'current_weather' (older) support
        temp = None
        if "current" in wd and wd["current"].get("temperature_2m") is not None:
            temp = wd["current"]["temperature_2m"]
        elif wd.get(
                "current_weather"
        ) and wd[
            "current_weather"
        ].get("temperature") is not None:
            temp = wd["current_weather"]["temperature"]
        return float(temp) if temp is not None else None
    except Exception:
        return None


@router.post("/update", status_code=status.HTTP_201_CREATED)
async def update_all_cities_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    if not cities:
        raise HTTPException(
            status_code=400,
            detail="No cities in database to update temperatures for."
        )
    results = []
    async with httpx.AsyncClient(timeout=15.0) as client:
        for city in cities:
            t = await _fetch_city_temperature(client, city)
            if t is not None:
                rec = models.Temperature(
                    city_id=city.id,
                    temperature=t,
                    date_time=datetime.now(timezone.utc)
                )
                db.add(rec)
                results.append({"city": city.name, "temperature": t})
        db.commit()
    return {"updated": len(results), "records": results}


@router.get("", response_model=List[schemas.TemperatureOut])
def list_temperatures(
        city_id: Optional[int] = Query(None, description="Filter by city_id"),
        db: Session = Depends(get_db),
):
    q = db.query(models.Temperature)
    if city_id is not None:
        q = q.filter(models.Temperature.city_id == city_id)
    return q.order_by(
        models.Temperature.date_time.desc(), models.Temperature.id.desc()
    ).all()
