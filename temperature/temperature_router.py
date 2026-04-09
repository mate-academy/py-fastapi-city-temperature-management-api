import asyncio
from datetime import timezone, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city.models import City
from city.crud import get_city
from dependencies import get_db
from temperature import models
from temperature import crud
from temperature.schemas import Temperature


router = APIRouter()

@router.post("/temperatures/update/")
async def update_temperature(db: Session = Depends(get_db)):
    cities = db.query(City).all()

    tasks = [crud.fetch_temperature(city.name) for city in cities]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for city, data in zip(cities, results):
        if isinstance(data, Exception):
            print(f"Error for {city.name}: {data}")
            continue

        temperature = models.Temperature(
            city_id=city.id,
            date_time=datetime.now(timezone.utc),
            temperature=data["current"]["temp_c"]
        )
        db.add(temperature)

    db.commit()

    return {"status": "updated"}


@router.get("/temperatures/", response_model=list[Temperature])
def get_temperature_list(
    city_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if city_id:
        return crud.get_city_temperature(db, city_id)
    return crud.get_temperature_list(db)
