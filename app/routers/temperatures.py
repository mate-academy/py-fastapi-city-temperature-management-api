import asyncio
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import crud, schemas, services
from app.database import get_db

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post("/update", status_code=status.HTTP_200_OK)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db, limit=1000)
    if not cities:
        return {"message": "There are no cities in the database to update."}

    tasks = [services.fetch_temperature_for_city(city.name) for city in cities]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    records_created = 0
    now = datetime.utcnow()

    for city, temp_value in zip(cities, results):
        if isinstance(temp_value, float):
            crud.create_temperature_record(
                db,
                city_id=city.id,
                temp_value=temp_value,
                timestamp=now
            )
            records_created += 1

    return {
        "status": "success",
        "message": f"Successfully updated temperatures for {records_created}/{len(cities)} cities."
    }


@router.get("", response_model=List[schemas.Temperature])
def read_temperatures(
    city_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):

    return crud.get_temperatures(db, city_id=city_id, skip=skip, limit=limit)
