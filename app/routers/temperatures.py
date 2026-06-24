from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas, models
from app.database import get_db
import httpx
import asyncio

router = APIRouter()


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = []
        for city in cities:
            url = f"https://wttr.in/{city.name}?format=j1"
            tasks.append(client.get(url))
        responses = await asyncio.gather(*tasks, return_exceptions=True)
    results = []
    for resp, city in zip(responses, cities):
        if isinstance(resp, Exception):
            continue
        if resp.status_code != 200:
            continue
        data = resp.json()
        current = data.get("current_condition")
        if not current:
            continue
        temp_c = current[0].get("temp_C")
        try:
            temp_val = float(temp_c)
        except Exception:
            continue
        temp = crud.create_temperature(db, city.id, temp_val)
        results.append(temp)
    return results


@router.get("/", response_model=List[schemas.TemperatureRead])
def list_temperatures(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    temps = crud.get_temperatures(db, city_id)
    return temps