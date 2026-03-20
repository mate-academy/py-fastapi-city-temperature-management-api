from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import asyncio
from .. import models, schemas
from ..database import get_db
from ..services import fetch_temperature_for_city

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post("/update", status_code=200)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    if not cities:
        raise HTTPException(status_code=400, detail="No cities found in the database.")

    tasks = [fetch_temperature_for_city(city.name) for city in cities]
    results = await asyncio.gather(*tasks)

    updated_count = 0
    failed_cities = []

    for city, temp in zip(cities, results):
        if temp is not None:
            new_record = models.Temperature(city_id=city.id, temperature=temp)
            db.add(new_record)
            updated_count += 1
        else:
            failed_cities.append(city.name)

    db.commit()

    return {
        "message": f"Updated temperatures for {updated_count} cities.",
        "failed_cities": failed_cities,
    }


@router.get("/", response_model=List[schemas.Temperature])
def get_temperatures(
    city_id: Optional[int] = Query(None), db: Session = Depends(get_db)
):
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()
