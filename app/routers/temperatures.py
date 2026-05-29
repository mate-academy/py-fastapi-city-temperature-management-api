from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import datetime
import httpx
from app import models, schemas, database

router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"]
)

async def fetch_mock_weather(city_name: str) -> float | None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://httpbin.org/delay/0")
            if response.status_code == 200:
                return float(15.0 + (len(city_name) % 15))
    except Exception:
        return 22.5


@router.post("/update", status_code=status.HTTP_200_OK)
async def update_temperatures(db: Session = Depends(database.get_db)) -> Dict[str, str]:
    cities = db.query(models.City).all()
    if not cities:
        raise HTTPException(status_code=400,
                            detail="No cities found in database to update.")

    records_added = 0
    for city in cities:
        current_temp = await fetch_mock_weather(city.name)

        temp_record = models.Temperature(
            city_id=city.id,
            temperature=current_temp,
            date_time=datetime.utcnow()
        )
        db.add(temp_record)
        records_added += 1

    db.commit()
    return {
        "message": f"Successfully updated temperature records for {records_added} cities."}


@router.get("/", response_model=List[schemas.TemperatureResponse])
def get_temperatures(city_id: Optional[int] = Query(None),
                     db: Session = Depends(database.get_db)) -> List[models.Temperature]:
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()
