from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import httpx
from datetime import datetime

from project.database import SessionLocal
from project import models, schemas

router = APIRouter(prefix="/temperatures", tags=["temperatures"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/update", response_model=list[schemas.Temperature])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()

    async with httpx.AsyncClient() as client:
        for city in cities:
            response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": city.latitude,
                    "longitude": city.longitude,
                    "current": "temperature_2m"
                }
            )

            if response.status_code != 200:
                continue

            data = response.json()
            temperatures = models.Temperature(
                city_id=city.id,
                temperature=data["current"]["temperature_2m"],
                date_time=datetime.now(),
            )
            db.add(temperatures)
    db.commit()

    return db.query(models.Temperature).all()


@router.get("/", response_model=list[schemas.Temperature])
def get_temperatures(city_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Temperature)
    if city_id:
        query = (query
                 .filter(models.Temperature.city_id == city_id))
    return query.all()