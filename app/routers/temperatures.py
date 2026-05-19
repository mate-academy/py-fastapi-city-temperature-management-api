from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import httpx
import json
import datetime

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()


@router.post("/update", response_model=List[schemas.TemperatureRead])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    results = []
    async with httpx.AsyncClient(timeout=10.0) as client:
        for city in cities:
            lat = None
            lon = None
            if city.additional_info:
                try:
                    info = json.loads(city.additional_info)
                    lat = info.get("lat") or info.get("latitude")
                    lon = info.get("lon") or info.get("longitude")
                except Exception:
                    # not JSON, skip coordinate extraction
                    pass

            if lat is None or lon is None:
                # skip cities without coordinates
                continue

            try:
                url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.json()
                current = data.get("current_weather")
                if not current:
                    continue
                temperature = float(current.get("temperature"))
                dt = datetime.datetime.utcnow()
                temp_obj = crud.create_temperature(db, city_id=city.id, temperature=temperature, date_time=dt)
                results.append(temp_obj)
            except httpx.HTTPError:
                continue

    return results


@router.get("/", response_model=List[schemas.TemperatureRead])
def list_temperatures(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id=city_id)
