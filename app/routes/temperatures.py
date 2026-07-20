import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies import get_db
from app import models, schemas
from app.services.weather import fetch_current_temperature

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", response_model=List[schemas.TemperatureOut])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found in the database")

    # Перевірка, що в усіх міст є координати
    missing_coords = [c.name for c in cities if c.latitude is None or c.longitude is None]
    if missing_coords:
        raise HTTPException(
            status_code=400,
            detail=f"Cities missing coordinates: {', '.join(missing_coords)}"
        )

    # Паралельний фетч температур для всіх міст одразу
    tasks = [fetch_current_temperature(city.latitude, city.longitude) for city in cities]
    temperatures = await asyncio.gather(*tasks, return_exceptions=True)

    new_records = []
    for city, temp in zip(cities, temperatures):
        if isinstance(temp, Exception):
            # Пропускаємо місто, якщо фетч впав, але не валимо весь запит
            continue
        record = models.Temperature(city_id=city.id, temperature=temp)
        db.add(record)
        new_records.append(record)

    db.commit()
    for record in new_records:
        db.refresh(record)

    return new_records


@router.get("", response_model=List[schemas.TemperatureOut])
def get_temperatures(
    city_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()
